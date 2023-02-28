import tango
from badger import interface
import os
# import time

class Interface(interface.Interface):

    name = 'tango-ctrm'

    tango_host = 'tango://acs.esrf.fr:10000/'

    os.environ['TANGO_HOST'] = 'acs.esrf.fr:10000'

    def __init__(self, params=None):
        super().__init__(params)

    @staticmethod
    def get_default_params():
        return None

    def get_value(self, attributename: str):

        attrprox = tango.AttributeProxy(self.tango_host + attributename)

        val = None
        if 'srdiag' in attributename:
            val = attrprox.read().value
        if 'srmag' in attributename:
            val = attrprox.read().w_value  # read set point

        return val

    def set_value(self, attributename: str, value: float):
        dev = tango.AttributeProxy(self.tango_host + attributename)
        dev.write(value)

