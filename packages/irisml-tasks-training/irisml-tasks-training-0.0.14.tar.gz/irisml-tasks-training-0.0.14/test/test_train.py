import collections
import unittest
import torch
from irisml.tasks.train.build_optimizer import OptimizerFactory
from irisml.tasks.train.build_lr_scheduler import LrSchedulerConfig, LrSchedulerFactory


class TestBuildOptimizer(unittest.TestCase):
    def test_create(self):
        self._check_build_optimizer('sgd', 0.001)
        self._check_build_optimizer('adam', 0.001)
        self._check_build_optimizer('amsgrad', 0.001)
        self._check_build_optimizer('adamw', 0.001)
        self._check_build_optimizer('adamw_amsgrad', 0.001)
        self._check_build_optimizer('rmsprop', 0.001)

    def test_no_weight_decay_param_names(self):
        model = torch.nn.Conv2d(3, 3, 3)

        factory = OptimizerFactory('sgd', 0.001, weight_decay=0.1, no_weight_decay_param_names=['.*bias'])
        optimizer = factory(model)
        w = collections.defaultdict(list)
        for group in optimizer.param_groups:
            w[group['weight_decay']].extend(group['params'])

        self.assertEqual(w, {0.1: [model.weight], 0.0: [model.bias]})

    def test_no_weight_decay_module_class_names(self):
        model = torch.nn.Sequential(torch.nn.Conv2d(3, 3, 3), torch.nn.BatchNorm2d(3))

        factory = OptimizerFactory('sgd', 0.001, weight_decay=0.1, no_weight_decay_module_class_names=['BatchNorm2d'])
        optimizer = factory(model)
        w = collections.defaultdict(list)
        for group in optimizer.param_groups:
            w[group['weight_decay']].extend(group['params'])

        self.assertEqual(w, {0.1: [model[0].weight, model[0].bias], 0.0: [model[1].weight, model[1].bias]})

    def _check_build_optimizer(self, *args):
        module = torch.nn.Conv2d(3, 3, 3)
        factory = OptimizerFactory(*args)
        optimizer = factory(module)
        self.assertIsInstance(optimizer, torch.optim.Optimizer)


class TestBuildLrScheduler(unittest.TestCase):
    def test_create(self):
        self._check_build_scheduler('cosine_annealing')
        self._check_build_scheduler('linear_decreasing')

    def test_warmup(self):
        config = LrSchedulerConfig('linear_decreasing', warmup_epochs=3, warmup_factor=0.1)
        factory = LrSchedulerFactory(config, num_epochs=10)
        # The first 3 epochs are warmup.
        self._assert_learning_rates(factory, 1, [0.1, 0.09, 0.08, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])

        config = LrSchedulerConfig('linear_decreasing', warmup_epochs=0.3, warmup_factor=0.1)
        factory = LrSchedulerFactory(config, num_epochs=10)
        # The first 3 epochs are warmup.
        self._assert_learning_rates(factory, 1, [0.1, 0.09, 0.08, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])

        config = LrSchedulerConfig('linear_decreasing', warmup_epochs=3, warmup_factor=0.1)
        factory = LrSchedulerFactory(config, num_epochs=10)
        # The first 3 epochs are warmup.
        self._assert_learning_rates(factory, 0.1, [0.01, 0.009, 0.008, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01])

    def _assert_learning_rates(self, lr_scheduler_factory, base_lr, expected_lrs):
        model = torch.nn.Conv2d(3, 3, 3)
        optimizer = torch.optim.SGD(model.parameters(), lr=base_lr)
        lr_scheduler = lr_scheduler_factory(optimizer)

        group = optimizer.param_groups[0]
        lrs = []
        for _ in range(10):
            optimizer.step()  # Call optimizer.step() to suppress the warnings.
            lrs.append(group['lr'])
            lr_scheduler.step()

        self._assert_almost_equal(lrs, expected_lrs)

    def _check_build_scheduler(self, name):
        model = torch.nn.Conv2d(3, 3, 3)
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

        factory = LrSchedulerFactory(LrSchedulerConfig(name), num_epochs=10)
        lr_scheduler = factory(optimizer)
        self.assertIsNotNone(lr_scheduler)

    def _assert_almost_equal(self, list1, list2):
        for i in range(len(list1)):
            self.assertAlmostEqual(list1[i], list2[i], msg=f"Expected: {list2}. Actual: {list1}")
        self.assertEqual(len(list1), len(list2))
