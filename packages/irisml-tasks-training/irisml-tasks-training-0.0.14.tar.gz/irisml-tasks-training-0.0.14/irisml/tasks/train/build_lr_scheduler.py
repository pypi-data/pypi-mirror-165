import dataclasses
import logging
import math
import typing
import torch

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class LrSchedulerConfig:
    name: str = 'cosine_annealing'
    warmup_epochs: typing.Optional[typing.Union[int, float]] = None
    warmup_factor: typing.Optional[float] = None


def build_lr_scheduler(config, optimizer, num_epochs):
    config = config or LrSchedulerConfig()

    scheduler = None
    if config.name == 'cosine_annealing':
        scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, num_epochs)
    elif config.name == 'linear_decreasing':
        scheduler = torch.optim.lr_scheduler.LinearLR(optimizer, start_factor=1, end_factor=0, total_iters=num_epochs)

    if not scheduler:
        raise ValueError(f"Unsupported lr scheduler name: {config.name}")

    if config.warmup_epochs and config.warmup_factor:
        warmup_epochs = config.warmup_epochs if isinstance(config.warmup_epochs, int) else math.ceil(num_epochs * config.warmup_epochs)
        logger.debug(f"Use learning rate warmup for {config.warmup_epochs} epochs. warmup_factor={config.warmup_factor}")
        warmup_scheduler = torch.optim.lr_scheduler.ConstantLR(optimizer, factor=config.warmup_factor, total_iters=warmup_epochs)
        scheduler = torch.optim.lr_scheduler.ChainedScheduler([scheduler, warmup_scheduler])

    return scheduler


class LrSchedulerFactory:
    def __init__(self, config: LrSchedulerConfig, num_epochs: int):
        self._config = config
        self._num_epochs = num_epochs

    def __call__(self, optimizer):
        return build_lr_scheduler(self._config, optimizer, self._num_epochs)
