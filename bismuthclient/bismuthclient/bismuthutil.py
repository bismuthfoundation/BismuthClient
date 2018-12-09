"""
Generic helpers  Bismuth
"""

import re
import hashlib
import base64

__version__ = '0.0.2'



def checksum(string):
    """ Base 64 checksum of MD5. Used by bisurl"""
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return base64.b85encode(m.digest()).decode("utf-8")


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

    @staticmethod
    def create_bis_url(recipient, amount, operation, openfield):
        """
        Constructs a bis url from tx elements
        """

        # Only command supported so far.
        command = "pay"
        openfield_b85_encode = base64.b85encode(openfield.encode("utf-8")).decode("utf-8")
        operation_b85_encode = base64.b85encode(operation.encode("utf-8")).decode("utf-8")
        url_partial = "bis://{}/{}/{}/{}/{}/".format(command,recipient,amount,operation_b85_encode,openfield_b85_encode)
        url_constructed = url_partial + checksum(url_partial)
        return url_constructed

    @staticmethod
    def read_url(url):
        """
        Takes a bis url, checks its checksum and gives the components
        """
        url_split = url.split("/")
        reconstruct = "bis://{}/{}/{}/{}/{}/".format(url_split[2],url_split[3],url_split[4],url_split[5],url_split[6],url_split[7])
        operation_b85_decode = base64.b85decode(url_split[5]).decode("utf-8")
        openfield_b85_decode = base64.b85decode(url_split[6]).decode("utf-8")

        if checksum(reconstruct) == url_split[7]:
            url_deconstructed = {"recipient": url_split[3], "amount": url_split[4], "operation": operation_b85_decode,
                                 "openfield": openfield_b85_decode}
            return url_deconstructed
        else:
            return {'Error': 'Checksum failed'}
