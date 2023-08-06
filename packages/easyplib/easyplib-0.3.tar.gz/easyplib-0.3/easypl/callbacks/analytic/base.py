import warnings
from typing import Dict

from pytorch_lightning.callbacks import Callback
from pytorch_lightning.loggers import WandbLogger


class BaseAnalyticCallback(Callback):
    def __init__(
            self,
            phase='train',
            save_on_disk=False
    ):
        self.phase = phase

        self.target_keys = None
        self.statistics = {}

    def __save_on_disk(self):
        for key in self.statistics:
            statistic = self.statistics[key]
            if statistic['type'] == 'plot':
                plot_image = self.__plot(self, )

    def __save_on_wandb(self):
        ...

    def __on_phase_start(self, trainer, pl_module):
        self.target_keys = pl_module.target_keys
        pl_module.return_output_phase[self.phase] = True

    def update_statistics(
            self,
            outputs: Dict,
            targets: Dict,
            dataloader_idx: int
    ):
        raise NotImplementedError

    def compute_statistics(
            self,
    ):
        raise NotImplementedError

    def __on_phase_batch_end(
            self,
            trainer,
            pl_module,
            outputs,
            batch,
            batch_idx,
            dataloader_idx,
    ):
        self.update_statistics(outputs['output'], outputs['target'], dataloader_idx)

    def on_train_start(self, trainer, pl_module):
        if self.phase == 'train':
            self.__on_phase_start(trainer, pl_module)

    def on_validation_start(self, trainer, pl_module):
        if self.phase == 'val':
            self.__on_phase_start(trainer, pl_module)

    def on_test_start(self, trainer, pl_module):
        if self.phase == 'test':
            self.__on_phase_start(trainer, pl_module)

    def on_predict_start(self, trainer, pl_module):
        if self.phase == 'predict':
            self.__on_phase_start(trainer, pl_module)

    def on_train_batch_end(
            self,
            trainer,
            pl_module,
            outputs,
            batch,
            batch_idx,
            dataloader_idx,
    ):
        if self.phase == 'train':
            self.__on_phase_batch_end(trainer, pl_module, outputs, batch, batch_idx, dataloader_idx)

    def on_validation_batch_end(
            self,
            trainer,
            pl_module,
            outputs,
            batch,
            batch_idx,
            dataloader_idx,
    ):
        if self.phase == 'val':
            self.__on_phase_batch_end(trainer, pl_module, outputs, batch, batch_idx, dataloader_idx)

    def on_test_batch_end(
            self,
            trainer,
            pl_module,
            outputs,
            batch,
            batch_idx,
            dataloader_idx,
    ):
        if self.phase == 'test':
            self.__on_phase_batch_end(trainer, pl_module, outputs, batch, batch_idx, dataloader_idx)

    def on_predict_batch_end(
            self,
            trainer,
            pl_module,
            outputs,
            batch,
            batch_idx,
            dataloader_idx,
    ):
        if self.phase == 'predict':
            self.__on_phase_batch_end(trainer, pl_module, outputs, batch, batch_idx, dataloader_idx)

    def __on_phase_epoch_end(
            self,
            trainer,
            pl_module
    ):
        self.compute_statistics()
        if isinstance(trainer.logger, WandbLogger):
            self.__save_on_wandb()
        else:
            warnings.warn(f'{trainer.logger.__class__.__name__} is not supported. Samples will log on disk.', Warning,
                          stacklevel=2)
            self.save_on_disk = True
        if self.save_on_disk:
            self.__save_on_disk()

    def on_train_epoch_end(
            self,
            trainer,
            pl_module,
            unused=False
    ):
        if self.phase == 'train':
            self.__on_phase_epoch_end(trainer, pl_module)

    def on_validation_epoch_end(
            self,
            trainer,
            pl_module
    ):
        if self.phase == 'val':
            self.__on_phase_epoch_end(trainer, pl_module)

    def on_test_epoch_end(
            self,
            trainer,
            pl_module
    ):
        if self.phase == 'test':
            self.__on_phase_epoch_end(trainer, pl_module)

    def on_predict_epoch_end(
            self,
            trainer,
            pl_module,
            unused=False
    ):
        if self.phase == 'predict':
            self.__on_phase_epoch_end(trainer, pl_module)
