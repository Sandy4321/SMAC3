import time
import unittest

from smac.scenario.scenario import Scenario
from smac.utils import test_helpers
from smac.smbo.smbo import SMBO, get_types
from smac.runhistory.runhistory2epm import RunHistory2EPM4EIPS
from smac.epm.uncorrelated_mo_rf_with_instances import \
    UncorrelatedMultiObjectiveRandomForestWithInstances
from smac.smbo.acquisition import EIPS
from smac.tae.execute_func import ExecuteTAFunc


def test_function(conf):
    x = conf['x']
    y = conf['y']
    runtime = y / 150.
    time.sleep(runtime)
    return x - y


class TestEIPS(unittest.TestCase):
    def test_eips(self):
        scenario = Scenario({'cs': test_helpers.get_branin_config_space(),
                             'run_obj': 'quality',
                             'deterministic': True})
        types = get_types(scenario.cs, None)
        umrfwi = UncorrelatedMultiObjectiveRandomForestWithInstances(
            ['cost', 'runtime'], types)
        eips = EIPS(umrfwi)
        rh2EPM = RunHistory2EPM4EIPS(scenario, 2)
        taf = ExecuteTAFunc(test_function)
        smbo = SMBO(scenario, model=umrfwi, acquisition_function=eips,
                    runhistory2epm=rh2EPM, tae_runner=taf)
        smbo.run(5)
        print(smbo.incumbent)
        raise ValueError()
