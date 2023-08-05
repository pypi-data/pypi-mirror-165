from argparse import ArgumentParser, Namespace

import pytest
import pytorch_lightning as pl
import torch
from torch.optim import AdamW
from transformers import BertTokenizer

from tests.helpers import DummyDataModule, DummyTransformerModel, standard_args
from transformers_lightning.schedulers import (
    ConstantScheduler,
    ConstantSchedulerWithWarmup,
    CosineSchedulerWithWarmup,
    CosineSchedulerWithWarmupAndHardRestart,
    LinearScheduler,
    LinearSchedulerWithWarmup,
)


@pytest.mark.parametrize(
    "scheduler_class, parameters, expected_lrs", (
        [
            ConstantSchedulerWithWarmup, {
                'num_warmup_steps': 5
            },
            [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        ], [
            ConstantScheduler, {},
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        ], [
            CosineSchedulerWithWarmupAndHardRestart,
            {
                'num_warmup_steps': 5,
                'num_training_steps': 20,
                'num_cycles': 2.0
            },
            [
                0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.9567727288213004, 0.8345653031794291, 0.6545084971874737,
                0.44773576836617335, 0.2500000000000001, 0.09549150281252633, 0.010926199633097156, 0.9890738003669028,
                0.9045084971874737, 0.7500000000000002, 0.552264231633827, 0.3454915028125262, 0.16543469682057088,
                0.04322727117869951, 0.0
            ],
        ], [
            CosineSchedulerWithWarmup, {
                'num_warmup_steps': 5,
                'num_training_steps': 20,
                'num_cycles': 0.5
            },
            [
                0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.9890738003669028, 0.9567727288213004, 0.9045084971874737,
                0.8345653031794291, 0.75, 0.6545084971874737, 0.5522642316338268, 0.44773576836617335,
                0.34549150281252633, 0.2500000000000001, 0.16543469682057105, 0.09549150281252633, 0.04322727117869951,
                0.010926199633097156, 0.0
            ]
        ], [
            LinearSchedulerWithWarmup, {
                'num_warmup_steps': 10,
                'num_training_steps': 20
            },
            [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
        ], [
            LinearScheduler, {
                'num_training_steps': 20
            },
            [
                1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1,
                0.05, 0.0
            ]
        ]
    )
)
def test_schedulers(scheduler_class, parameters, expected_lrs):

    hyperparameters = Namespace(
        batch_size=1,
        val_batch_size=1,
        test_batch_size=1,
        num_workers=0,
        max_epochs=1,
        max_steps=20,
        scheduler_last_epoch=-1,
        scheduler_verbose=False,
        accelerator='cpu',
        iterable=False,
        log_every_n_steps=1,
        accumulate_grad_batches=1,
        **standard_args,
        **parameters,
    )

    scheduler_class.add_argparse_args(ArgumentParser())

    class SchedulerModel(DummyTransformerModel):

        def __init__(self, hyperparameters):
            super().__init__(hyperparameters)
            self.lrs = []

        def _get_actual_lr(self):
            return self.trainer.optimizers[0].__dict__['param_groups'][0]['lr']

        def training_step(self, batch, *args):
            res = super().training_step(batch, *args)
            return {**res, 'lr': self._get_actual_lr()}

        def training_epoch_end(self, outputs, *args, **kwargs):
            self.lrs = [o['lr'] for o in outputs] + [self._get_actual_lr()]

        def configure_optimizers(self):
            # Define adam optimizer
            optimizer = AdamW(self.model.parameters(), lr=1.0)
            scheduler = scheduler_class(hyperparameters, optimizer)

            return {
                'optimizer': optimizer,
                'lr_scheduler': {
                    'scheduler': scheduler,
                    'interval': 'step',
                    'frequency': 1
                }
            }

    tokenizer = BertTokenizer('tests/data/vocab.txt')

    # instantiate PL trainer and model
    trainer = pl.Trainer.from_argparse_args(hyperparameters)
    model = SchedulerModel(hyperparameters)

    # Datasets and Fit
    datamodule = DummyDataModule(hyperparameters, length_train=96, tokenizer=tokenizer)
    trainer.fit(model, datamodule=datamodule)

    assert torch.allclose(
        torch.tensor(expected_lrs),
        torch.tensor(model.lrs),
    ), (f"{expected_lrs} vs {model.lrs}")
