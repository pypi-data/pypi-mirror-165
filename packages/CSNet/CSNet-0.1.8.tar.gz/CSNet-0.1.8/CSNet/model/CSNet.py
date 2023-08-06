import torch
from torch import nn, zero_
import torch.nn.functional as F
from torch.autograd import Variable
from torch.nn import Linear, Mish, Parameter, Sequential, Module
from torch.distributions import Normal, Poisson
from scvi.nn import DecoderSCVI

from ._criterion import Loss
from ._gumbel import gumbel_sigmoid


class Encoder(Module):
    def __init__(self,
                 snr: float = 5,
                 in_dim: int = 1200,
                 m_dim: int = 100,
                 bias: float = 0.0,
                 **kwargs):
        super().__init__()
        self.snr = snr
        self.t = nn.Parameter(torch.tensor([1.]))
        self.enc_net = Sequential(Linear(in_dim, m_dim-1))
        self.A = nn.Parameter(torch.randn(in_dim, m_dim-1))
        nn.init.xavier_normal_(self.A)
        self.hard = False
        self.use_noise = True
        self.bias = bias

    def forward(self, x):
        # noise = torch.randn(x.shape[0], x.shape[1]).to(x.device)
        # noise *= torch.linalg.norm(x) / \
        #     torch.linalg.norm(noise)*(torch.tensor(10**(self.snr/20)))
        # x = x + noise
        A = gumbel_sigmoid(self.A, self.t.detach(),
                           self.hard, self.use_noise, 
                           self.bias)
        # y = self.enc_net(x)
        # A = self.A
        y = x.mm(A)
        A_loss = A.pow(2).sum(-1).mean()

        return A_loss, y


class CSNet(Module):
    def __init__(self,
                 lambda_sparsity: float = 1,
                 lambda_cos: float = 1,
                 **kwargs):
        super().__init__()

        self.m_dim = kwargs['m_dim']
        self.in_dim = kwargs['in_dim']
        self.lambda_sparsity = lambda_sparsity
        self.lambda_cos = lambda_cos
        self.encoder = Encoder(**kwargs)
        self.decoder = DecoderSCVI(
            n_input=self.m_dim-1, n_output=self.in_dim)
        self.px_r = torch.nn.Parameter(torch.randn(self.in_dim))
        self.recon = Loss().recon
        self.sigma = 0.01
        
    def z_sample(self, y, library, use_mu=False, **kwargs):
        y = torch.log(1+y)
        mu = y
        std = self.sigma
        eps = torch.randn_like(mu)
        z = eps.mul(std).add_(mu)

        px_scale, px_r, px_rate, px_dropout = self.decoder(
            "gene",
            mu if use_mu else z,
            library[:, None],
        )
        
        return px_scale, px_r, px_rate, px_dropout

    def loss_update(self, x, px_rate, px_r, px_dropout, **kwargs):
        loss_dict = {}
        # loss_dict['A_loss'] = 0.  # A_loss
        xhat, loss_dict['recon_loss'] = self.recon(
            recon_type='ZINB', target=x, px_rate=px_rate, px_r=px_r, px_dropout=px_dropout)
        loss_dict['cos_loss'] = (
            1-F.cosine_similarity(x, px_rate, dim=1)).sum()
        loss_dict['cos_loss2'] = (
            1-F.cosine_similarity(x, px_rate, dim=0)).sum()

        loss_dict['loss'] = 0
        for loss_str, lambda_ in zip(['recon_loss', 'cos_loss', 'cos_loss2'], [1, self.lambda_cos, self.lambda_cos]):
            loss_ = loss_dict[loss_str]
            # / (loss_/loss_dict['recon_loss']).detach()
            loss_ = loss_ * lambda_
            loss_dict['loss'] += loss_
        
        return xhat, loss_dict
    
    def forward1(self, batch, use_mu, **kwargs):
        x, library = batch
        A_loss, y = self.encoder(x)
        px_scale, px_r, px_rate, px_dropout = self.z_sample(y, library, use_mu)
        px_r = torch.exp(self.px_r)
        xhat, loss_dict = self.loss_update(x, px_rate, px_r, px_dropout)

        return xhat, px_rate, loss_dict
    
    def forward2(self, batch, use_mu, A, **kwargs):
        x, library = batch
        A = A.to(x.device)
        y = x.mm(A)
        px_scale, px_r, px_rate, px_dropout = self.z_sample(y, library, use_mu)
        px_r = torch.exp(self.px_r)
        xhat, loss_dict = self.loss_update(x, px_rate, px_r, px_dropout)

        return xhat, px_rate, loss_dict
    
    def forward3(self, batch, use_mu, **kwargs):
        y, library = batch
        px_scale, px_r, px_rate, px_dropout = self.z_sample(y, library, use_mu)

        return None, px_rate, None
    
if __name__ == '__main__':
    # python -m CSNet.model.CSNet
    from ..data.dataset import DataLight
    from ..function import getMinUsedGPU
    data_path = '/data/xizhu/shen/ST/CSNet/data/scvi'
    gpus = getMinUsedGPU()
    dataLight = DataLight(data_path, gpus)
    train_loader = dataLight.train_dataloader()
    model = CSNet(
        in_dim=dataLight.gene_dim, m_dim=100, snr=5, hidden_dim=200)
    iter_ = iter(train_loader)
    model.forward(next(iter_))
    print(model)
