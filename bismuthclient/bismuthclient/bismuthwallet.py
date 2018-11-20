"""
A class encapsulating a Bismuth wallet (keys, address, crypto functions)

WIP
"""

import json
import logging

from os import path
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA
import getpass

__version__ = '0.0.2'


class BismuthWallet():

    __slots__ = ('_address', '_wallet_file', 'verbose', '_encrypted', '_infos', "verbose")

    def __init__(self, wallet_file='wallet.der', verbose=False):
        self._wallet_file = None
        self._address = None
        self._infos = None
        self.verbose = verbose
        self.load(wallet_file)

    def wallet_preview(self, wallet_file='wallet.der'):
        """
        Returns info about a wallet without actually loading it.
        """
        info = {'file': wallet_file, 'address': '', 'encrypted': False}
        try:
            with open(wallet_file, 'r') as f:
                content = json.load(f)
            info['address'] = content['Address']  # Warning case change!!!
            try:
                key = RSA.importKey(content['Private Key'])
                info['encrypted'] = False
            except:  # encrypted
                info['encrypted'] = True
        except:
            pass
        return info

    def info(self):
        """
        Returns a dict with info about the current wallet.
        :return:
        """
        return self._infos

    def load(self, wallet_file='wallet.der'):
        """
        Loads the wallet.der file

        :param wallet_file: string, a wallet file path
        """
        if self.verbose:
            print("Load", wallet_file)
        self._wallet_file = None
        self._address = None
        self._infos = {"address": '', 'file': wallet_file, 'encrypted': False}
        if not path.isfile(wallet_file):
            return

        self._wallet_file = wallet_file
        with open(wallet_file, 'r') as f:
            content = json.load(f)
            self._infos['address'] = content['Address']  # Warning case change!!!
            self._address = content['Address']
        try:
            key = RSA.importKey(content['Private Key'])
        except:  # encrypted
            self._infos['encrypted'] = True

    @property
    def address(self):
        """Returns the currently loaded address, or None"""
        return self._address
