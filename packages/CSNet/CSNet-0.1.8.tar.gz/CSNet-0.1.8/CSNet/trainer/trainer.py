import sys
import os
from tkinter import N
from tqdm import tqdm
import yaml
import torch
import wandb
import numpy as np
import pytorch_lightning as pl
from ..experiment.experiment import ExprLight
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from ..function import getMinUsedGPU, correlations
from ..model._gumbel import gumbel_sigmoid
import pandas as pd
import wandb
import gc

import os
import yaml
import wandb

class Trainer(object):
    def __init__(self, output_dir: str = None, project: str = 'CS', entity: str = 'ustcszq'):
        self.output_dir = output_dir
        self.project = project
        self.entity = entity

    def wandb_init(self, WANDB_MODE: str, file: str, wandb_use=True):
        os.environ["WANDB_MODE"] = WANDB_MODE
        if wandb_use:
            self.wandb_run = wandb.init(
                project=self.project,
                entity=self.entity,
                config=os.path.join(self.output_dir, file),
                settings=wandb.Settings(start_method='thread')
            )
            config = wandb.config
        else:
            with open(os.path.join(self.output_dir, file)) as f:
                config = yaml.load(f, yaml.SafeLoader)
            self.wandb_run = wandb.init(
                project=self.project,
                entity=self.entity,
                config=config,
                settings=wandb.Settings(start_method='thread'))
        assert config['m_dim']>2, 'The number of measurement channels must be greater than 2'
        torch.manual_seed(config['manual_seed'])
        np.random.seed(config['manual_seed'])
        config['gpus'] = getMinUsedGPU()
        config['output_dir'] = self.output_dir

        self.config = config

    def experiment_init(self, save_top_k=3, patience=5, mode='min', monitor='val/loss', max_epochs=100, model_path=None, **config):
        experiment = ExprLight(**config)

        wandb_logger = WandbLogger(
            save_dir='wandb'
        )

        early_stopping = EarlyStopping(
            monitor=monitor,
            mode=mode,
            patience=patience
        )

        checkpoint_callback = ModelCheckpoint(
            monitor=monitor,
            dirpath=os.path.join(wandb_logger.experiment.dir, '../checkpoint'),
            filename="{epoch:02d}-{val_loss:.2e}",
            save_top_k=save_top_k,
            mode=mode,
        )

        runner = pl.Trainer(
            strategy='dp',
            precision=32,
            benchmark=True,
            limit_train_batches=1.0,  # 控制数据集读入比例
            limit_val_batches=1.0,
            limit_test_batches=1.0,
            log_every_n_steps=100,
            logger=wandb_logger,
            callbacks=[early_stopping, checkpoint_callback],
            check_val_every_n_epoch=1,
            num_sanity_val_steps=0,
            max_epochs=max_epochs,
            gpus=config['gpus'],
        )
        if model_path:
            ckpt = torch.load(model_path)
            experiment.load_state_dict(ckpt['state_dict'])
            experiment.A = gumbel_sigmoid(ckpt['state_dict']['model.encoder.A'],
                                          ckpt['state_dict']['model.encoder.t'],
                                          True,
                                          True,
                                          self.config['bias'])

        self.wandb_logger = wandb_logger
        self.early_stopping = early_stopping
        self.early_stopping = early_stopping
        self.checkpoint_callback = checkpoint_callback
        self.experiment = experiment
        self.runner = runner

    def yaml_write(self, config):
        model_path = self.checkpoint_callback.best_model_path
        if type(config) != dict:
            config = config.as_dict()
        config['model_path'] = model_path
        if self.experiment.step == 1:
            config['step'] = 2
        elif self.experiment.step == 2:
            config['step'] = 3
            config['test_path'] = os.path.join(self.output_dir, 'test_M.h5ad')
        else:
            return
        with open(os.path.join(self.output_dir, 'step%s.yaml' % config['step']), 'w') as f:
            yaml.dump(config, f)
        with open(os.path.join(self.experiment.save_dir, 'step%s.yaml' % config['step']), 'w') as f:
            yaml.dump(config, f)

    def step1(self, WANDB_MODE='offline'):
        self.wandb_init(WANDB_MODE, 'step1.yaml', wandb_use=True)
        self.experiment_init(**self.config)
        self.runner.fit(self.experiment)
        self.runner.test(ckpt_path='best')
        self.yaml_write(self.config)
        wandb.finish()

    def step2(self, WANDB_MODE='offline'):
        self.wandb_init(WANDB_MODE, 'step2.yaml', wandb_use=False)
        self.experiment_init(**self.config)
        self.runner.fit(self.experiment)
        self.runner.test(ckpt_path='best')
        self.yaml_write(self.config)
        self.result_save()
        wandb.finish()

    def step3(self):
        self.wandb_init('offline', 'step3.yaml', wandb_use=False)
        assert self.config['model_path'] != None, 'model_path is None'
        self.experiment_init(**self.config)
        self.runner.test(self.experiment)
        wandb.finish()

    def result_save(self):
        save_dir = self.experiment.save_dir
        print('save_dir:', save_dir)

        A = self.experiment.A.detach().cpu().numpy().T
        A_ = np.concatenate([A, np.ones((1, A.shape[1]))], axis=0)
        np.save(os.path.join(save_dir, 'phi.npy'), A_)
        self.wandb_run.log({'density': A_.sum()/A_.shape[0]/A_.shape[1]})
        print('A_density:', A_.sum()/A_.shape[0]/A_.shape[1])

        adata = self.experiment.dataset.dataset_test.adata
        adata.obsm['measurements'] = adata.layers['counts'].dot(A.T)
        adata.obsm['library'] = adata.layers['counts'].sum(-1)
        adata.write(os.path.join(self.output_dir, 'test_M.h5ad'))
        print('Save pseudo measurements')

        gene_dict = {}
        for i in range(len(A)):
            genes = adata.var_names[A[i] > 0].tolist()
            gene_dict['Measurement %s' % i] = genes
        gene_dict['Library'] = adata.var_names.tolist()
        np.save(os.path.join(save_dir, 'genes.npy'), gene_dict)
        print('Save genenames of measurements')

