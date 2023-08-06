from lib2to3.pgen2.pgen import generate_grammar
import os
import gc
from turtle import forward
import wandb
import torch
import numpy as np
import pandas as pd
from torch import optim
from scipy import sparse
from ..model.CSNet import CSNet
import pytorch_lightning as pl
from ..data.dataset import DataLight
from pytorch_lightning import Trainer
from anndata._core.aligned_mapping import I
from sklearn.metrics import adjusted_rand_score
from pytorch_lightning.loggers import TestTubeLogger, TensorBoardLogger, CometLogger, WandbLogger
import numpy as np
from ..function import correlations, compare_results, get_observations
from scipy.stats import pearsonr
from scipy.spatial import distance
from ..model._gumbel import gumbel_sigmoid


class ExprLight(pl.LightningModule):
    def __init__(self,
                 LR: float = 0.001,
                 weight_decay: float = 0,
                 scheduler_gamma: float = None,
                 output_dir: str = None,
                 **kwargs):
        super().__init__()
        self.LR = LR
        self.t_decay = kwargs['t_decay']
        self.weight_decay = weight_decay
        self.scheduler_gamma = scheduler_gamma
        self.snr = kwargs['snr']
        self.step = kwargs['step']
        self.output_dir = output_dir
        self.A = None

        self.dataset = DataLight(**kwargs)
        kwargs['in_dim'] = self.dataset.gene_dim
        self.model = CSNet(**kwargs)

        self.x = []
        self.mu = []

    def forward(self, batch, use_mu=False, **kwargs):
        if self.step == 1:
            forward = self.model.forward1
        elif self.step == 2:
            forward = self.model.forward2
        elif self.step == 3:
            forward = self.model.forward3
        else:
            assert False, 'step must be 1, 2 or 3'

        results = forward(batch, use_mu, A=self.A)
        return results

    def training_step(self, batch, batch_idx, optimizer_idx=0):
        self.model.encoder.hard = False
        self.model.encoder.use_noise = True
        xhat, mu, loss_dict = self.forward(batch)

        for key in loss_dict.keys():
            self.log('train/' + key, loss_dict[key], on_epoch=True)

        return loss_dict['loss']

    def validation_step(self, batch, batch_idx, optimizer_idx=0):
        self.model.encoder.hard = True
        self.model.encoder.use_noise = True
        xhat, mu, loss_dict = self.forward(batch)

        return loss_dict

    def validation_epoch_end(self, outputs):
        self.model.encoder.t *= self.t_decay
        for key in outputs[0].keys():
            loss = torch.stack([x[key] for x in outputs]).mean()
            self.log('val/' + key, loss, on_step=False, on_epoch=True)
            if key == 'loss':
                self.log('val_' + key, loss, on_step=False, on_epoch=True)

    def test_step(self, batch, batch_idx, optimizer_idx=0):
        self.model.encoder.hard = True
        self.model.encoder.use_noise = True
        xhat, mu, loss_dict = self.forward(batch, use_mu=True)
        self.mu.append(mu)
        self.x.append(batch[0])
        return loss_dict

    def test_epoch_end(self, outputs):
        if self.step != 3:
            self.test_save_log(outputs)
        else:
            mu = torch.cat(self.mu).cpu().numpy()
            self.predict = mu
            np.save(os.path.join(self.output_dir, 'predict_M.npy'), mu)
        self.x = []
        self.mu = []

    def phi_optimize(self):
        A = gumbel_sigmoid(self.model.encoder.A,
                           self.model.encoder.t,
                           True,
                           True,
                           self.model.encoder.bias).T
        A = A.detach().cpu().numpy()

        for dataset in [self.dataset.dataset_val, self.dataset.dataset_test]:
            dataset.count = dataset.adata.layers['counts'].toarray().dot(A.T)

        return A

    def test_save_log(self, outputs):
        for key in outputs[0].keys():
            loss = torch.stack([x[key] for x in outputs]).mean()
            self.log('test/' + key, loss, on_step=False, on_epoch=True)

        x = torch.cat(self.x).cpu().numpy()
        mu = torch.cat(self.mu).cpu().numpy()

        columns = ['overallPearson', 'overallSpearman', 'genePearson', 'cellPearson',
                   'cellDistPearson', 'cellDistSpearman', 'geneDistPearson', 'geneDistSpearman']
        corrs = compare_results(x.T.astype(np.float64),
                                mu.T.astype(np.float64))

        # df = pd.DataFrame(zip(columns, corrs), columns=['metric', 'value'])
        # df.to_csv(os.path.join(self.save_dir, 'correlations.csv'), index=False)

        for i, corr in zip(columns, corrs):
            # print(i+':', corr)
            self.log(i, corr, on_step=False, on_epoch=True)

        np.save(os.path.join(self.output_dir, 'target.npy'), x)
        np.save(os.path.join(self.output_dir, 'predict.npy'), mu)
        gc.collect()

        self.target = x
        self.predict = mu
        self.correlations = corrs

    def getSaveDIR(self):
        # save result
        if isinstance(self.logger, WandbLogger):
            self.save_dir = os.path.join(
                self.logger.experiment.dir, '../result')
        if isinstance(self.logger, TensorBoardLogger):
            self.save_dir = self.logger.log_dir
        try:
            os.mkdir(self.save_dir)
        except:
            pass

    def configure_optimizers(self):
        self.getSaveDIR()
        optims = []
        scheds = []

        optimizer = optim.Adam(self.model.parameters(),
                               lr=self.LR,
                               betas=(0.9, 0.99),
                               eps=1e-06,
                               weight_decay=self.weight_decay)
        optims.append(optimizer)

        try:
            if self.scheduler_gamma is not None:
                scheduler = optim.lr_scheduler.ExponentialLR(
                    optims[0], gamma=self.scheduler_gamma)
                scheds.append(scheduler)
                return optims, scheds
        except:
            return optims

    def train_dataloader(self):
        return self.dataset.train_dataloader()

    def val_dataloader(self):
        return self.dataset.val_dataloader()

    def test_dataloader(self):
        return self.dataset.test_dataloader()


if __name__ == '__main__':
    # python -m CSNet.experiment.experiment
    from ..data.dataset import DataLight
    kwargs = {
        'LR': 0.001,
        'weight_decay': 0,
        'm_dim': 100,
        'snr': 5,
        'hidden_dim': 500,
        'data_path': '/data/xizhu/shen/ST/CSNet/data/scvi',
        'gpus': [0]
    }
    expr = ExprLight(**kwargs)
    print(expr)

    runner = Trainer(max_epochs=1)
    runner.fit(expr)
    runner.test(ckpt_path='best')
