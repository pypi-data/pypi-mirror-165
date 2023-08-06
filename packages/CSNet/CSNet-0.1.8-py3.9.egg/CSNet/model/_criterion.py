import torch
from torch import nn
import torch.nn.functional as F
from scvi.distributions import NegativeBinomial, ZeroInflatedNegativeBinomial
from torch.distributions import Normal, Poisson


class Loss(object):
    def __init__(self):
        self.recon_funcs = {
            'MSE': self.MSE_recon,
            'Normal': self.Normal_recon,
            'Poisson': self.Poisson_recon,
            'NB': self.NB_recon,
            'ZINB': self.ZINB_recon,
        }

    def MSE_recon(self, target, pred, **kwargs):
        recon_loss = nn.MSELoss()(pred, target)

        return recon_loss

    def Normal_recon(self, target, pred,**kwargs):
        scale = torch.ones_like(pred)
        dist = torch.distributions.Normal(pred, scale)
        recon_loss = (-dist.log_prob(target)).sum(-1).mean()
        pred = dist.sample()

        return pred, recon_loss

    def Poisson_recon(self, target, pred, **kwargs):
        pred = nn.functional.softplus(pred)
        dist = Poisson(mu=pred)
        recon_loss = (-dist.log_prob(target)).sum(-1).mean()

        return pred, recon_loss

    def NB_recon(self, target, px_rate, px_r, **kwargs):
        # pred = nn.functional.softplus(pred)
        dist = NegativeBinomial(mu=px_rate, theta=px_r)
        recon_loss = (-dist.log_prob(target)).sum(-1).mean()
        pred = dist.sample()

        return pred, recon_loss
    
    def ZINB_recon(self, target, px_rate, px_r, px_dropout, **kwargs):
        dist = ZeroInflatedNegativeBinomial(
                mu=px_rate, theta=px_r, zi_logits=px_dropout
            )
        recon_loss = (-dist.log_prob(target)).sum(-1).mean()
        pred = dist.sample()
        
        return pred, recon_loss

    def recon(self, recon_type, target, **kwargs):
        if recon_type in self.recon_funcs.keys():
            pred, recon_loss = self.recon_funcs[recon_type](
                target, **kwargs)
            return pred, recon_loss
        else:
            raise ValueError('recon_type is not defined')
    