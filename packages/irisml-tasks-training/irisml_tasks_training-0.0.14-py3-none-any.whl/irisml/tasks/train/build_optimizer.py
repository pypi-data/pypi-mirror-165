import logging
import re
import torch.optim

logger = logging.getLogger(__name__)


def build_optimizer(name: str, parameters, base_lr, weight_decay, momentum):
    if name == 'sgd':
        return torch.optim.SGD(parameters, lr=base_lr, weight_decay=weight_decay, momentum=momentum)
    elif name == 'adam':
        return torch.optim.Adam(parameters, lr=base_lr, weight_decay=weight_decay)
    elif name == 'amsgrad':
        return torch.optim.Adam(parameters, lr=base_lr, weight_decay=weight_decay, amsgrad=True)
    elif name == 'adamw':
        return torch.optim.AdamW(parameters, lr=base_lr, weight_decay=weight_decay)
    elif name == 'adamw_amsgrad':
        return torch.optim.AdamW(parameters, lr=base_lr, weight_decay=weight_decay, amsgrad=True)
    elif name == 'rmsprop':
        return torch.optim.RMSprop(parameters, lr=base_lr, weight_decay=weight_decay, momentum=momentum)
    else:
        raise ValueError(f"Unsupported optimizer: {name}")


class OptimizerFactory:
    def __init__(self, name: str, base_lr, weight_decay=0, momentum=0, no_weight_decay_param_names=None, no_weight_decay_module_class_names=None):
        self._name = name
        self._base_lr = base_lr
        self._weight_decay = weight_decay
        self._momentum = momentum
        self._no_weight_decay_param_name_patterns = [re.compile(p) for p in (no_weight_decay_param_names or [])]
        self._no_weight_decay_module_class_name_patterns = [re.compile(p) for p in (no_weight_decay_module_class_names or [])]

    def __call__(self, model):
        params = []
        no_weight_decay_params = set()

        for name, module in model.named_modules():
            if any(p.match(type(module).__name__) for p in self._no_weight_decay_module_class_name_patterns):
                logger.debug(f"Disabling weight_decay for module {name}")
                no_weight_decay_params.update(module.parameters())

        for name, param in model.named_parameters():
            if any(p.match(name) for p in self._no_weight_decay_param_name_patterns):
                logger.debug(f"Disabling weight_decay for param {name}")
                no_weight_decay_params.add(param)

        params = list(set(model.parameters()) - no_weight_decay_params)
        param_groups = []
        if params:
            param_groups.append({'params': params})
        if no_weight_decay_params:
            param_groups.append({'params': list(no_weight_decay_params), 'weight_decay': 0.0})

        return build_optimizer(self._name, param_groups, self._base_lr, self._weight_decay, self._momentum)
