"""
Generic helpers  Bismuth
"""

import re

__version__ = '0.0.1'


class BismuthUtil():
    """Static helper utils"""


    @staticmethod
    def valid_address(address: str):
        """Says if that address looks ok"""
        return re.match('[abcdef0123456789]{56}', address)

    @staticmethod
    def fee_for_tx(message=''):
        """Returns fee for the matching message"""
        return 0.01 + len(message) / 100000

    @staticmethod
    def height_to_supply(height):
        """Gives total supply at a given block height"""
        R0 = 11680000.4
        delta = 2e-6
        pos = 0.8
        pow = 12.6
        N = height - 8e5
        dev_rew = 1.1
        R = dev_rew * R0 + N * (pos + dev_rew * (pow - N / 2 * delta))
        return R

