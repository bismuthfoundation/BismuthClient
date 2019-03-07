"""
Formatting helpers and converters for Bismuth
"""

import datetime
# import re

__version__ = '0.0.33'


# TODO: common ancestor, factorize

class TxFormatter():
    """Formats a Bismuth Transaction"""

    __slots__ = ['tx']
    _tx_keys = ["block_height", "timestamp", "address", "recipient", "amount", "signature", "public_key", "block_hash",
                "fee", "reward", "operation", "openfield"]

    def __init__(self, tx):
        self.tx = tx

    def to_string(self):
        return str(self.tx)

    def to_json(self, for_display=False):
        json = dict(zip(self._tx_keys, self.tx))
        if for_display:
            json['datetime'] = datetime.datetime.utcfromtimestamp(json['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            json['amount'] = AmountFormatter(json['amount']).to_string()
            json['fee'] = AmountFormatter(json['fee']).to_string(leading=1)
            if json['operation'] == '0':
                json['operation'] = ''
        return json


class AmountFormatter():
    """Format a BIS amount to string"""

    __slots__ = ['amount']

    def __init__(self, amount):
        self.amount = float(amount)

    def to_string(self, decimals=3, leading=0):
        try:
            temp = round(self.amount, decimals)
            int_part, decimal_part = str(temp).split('.')
            while len(decimal_part) < decimals:
                decimal_part += '0'
            out = "{integer: >{fill}}.{decimal}".format(integer=int_part, decimal=decimal_part, fill=leading)
        except:
            out = '0.000'
        return out
