import time
import numpy as np
from badger import environment
from badger.interface import Interface


class Environment(environment.Environment):

    name = 'esrf-simulator'
    var_channel_map = {
        'sf2e-c30': 'srmag/sqp-sf2/c30-e/CorrectionStrength',
        'sf2a-c10': 'srmag/sqp-sf2/c10-a/CorrectionStrength',
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)

    @staticmethod
    def list_vars():
        return ['sf2e-c30', 'sf2a-c10']

    @staticmethod
    def list_obses():
        return ['vertical-emittance']

    @staticmethod
    def get_default_params():
        return {
            'waiting_time': 1,
        }

    def _get_var(self, var):
        return self.interface.get_value(self.var_channel_map[var])

    def _set_var(self, var, x):
        self.interface.set_value(self.var_channel_map[var], x)

    #def _check_var(self, var):
    #    if not self.params['chaos']:
    #        return 0

    #    time.sleep(0.1 * np.random.rand())
    #    return round(np.random.rand())

    def _get_vrange(self, var):
        return {'sf2e-c30': [-0.02, 0.02], 'sf2a-c10': [-0.02, 0.02]}[var]

    def _get_obs(self, obs):

        try:
            dt = self.params['waiting_time']
        except KeyError:
            dt = 0
        time.sleep(dt)

        if obs == 'vertical-emittance':
            return self.interface.get_value('srdiag/emittance/id07/Emittance_V')

