"""
A class encapsulating a Bismuth wallet (keys, address, crypto functions)

This is a wallet.json file that can embed many different addresses/keys and is globally encrypted by a master password.

WIP
"""

from base64 import b64encode, b64decode
import json
import random
from copy import deepcopy

from os import path
from time import time
from bismuthclient import bismuthcrypto
from bismuthclient.simplecrypt import encrypt, decrypt
from Cryptodome.PublicKey import RSA
# from Cryptodome.Signature import PKCS1_v1_5
# from Cryptodome.Hash import SHA
# import getpass
# import hashlib
import os, sys

__version__ = '0.0.2'


class BismuthMultiWallet():

    __slots__ = ('_address', '_wallet_file', 'verbose', '_infos', "verbose", "key", "public_key",
                 '_addresses', '_locked', '_data', '_master_password')

    def __init__(self, wallet_file: str='wallet.json', verbose: bool=False, seed: str=None):
        self._wallet_file = None
        self._address = None
        self._infos = None
        self.key = None
        self._data = None  # raw data
        self._locked = False
        self.public_key = ''
        self.verbose = verbose
        self._addresses = []  # clear data if unlocked
        self._master_password = ''
        self.load(wallet_file, seed=seed)

    def wallet_preview(self, wallet_file: str='wallet.json'):
        """
        Returns info about a wallet without actually loading it.
        """
        info = {'file': wallet_file, 'address': '', 'encrypted': False, 'count': 0}
        try:
            with open(wallet_file, 'r') as f:
                content = json.load(f)
            info['count'] = len(content['addresses'])
            info['encrypted'] = len(content['encrypted'])
        except:
            pass
        return info

    def info(self):
        """
        Returns a dict with info about the current wallet.
        :return:
        """
        return self._infos

    def load(self, wallet_file: str='wallet.json', seed: str=None):
        """
        Loads the wallet.json file

        :param wallet_file: string, a wallet file path
        :param seed: None or string, an optional seed for reproducible tests. Do NOT use in prod.
        """
        if self.verbose:
            print("Load Multi", wallet_file)
        self._wallet_file = None
        self._address = None
        self._infos = {"address": '', 'file': wallet_file, 'encrypted': False}
        if seed:
            random.seed(seed)
        if not path.isfile(wallet_file):
            charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&~#{([|-\_@)]=}+-*/<>!,;:.?%'
            salt = "".join(random.choice(charset) for x in range(random.randint(10, 20)))
            default = {"salt": salt, "spend": {"type": None, "value": None},
                       "version": __version__, "coin": "bis", "encrypted": False,
                       "addresses": []}
            with open(wallet_file, 'w') as f:
                json.dump(default, f)

        with open(wallet_file, 'r') as f:
            self._data = json.load(f)
            # No selected address by default.
            self._infos['address'] = ''
            self._address = ''
        self._infos['encrypted'] = self._data['encrypted']
        self._wallet_file = wallet_file
        # If our wallet
        self._locked = self._data['encrypted']
        self._master_password = ''
        if not self._locked:
            self._addresses = deepcopy(self._data['addresses'])
        else:
            self._addresses = []

    def save(self, wallet_file: str=None):
        if wallet_file is None:
            wallet_file = self._wallet_file
        with open(wallet_file, 'w') as f:
            json.dump(self._data, f)

    def encrypt(self, password:str='', current_password:str=None):
        """Encrypt - or re-encrypt """
        if len(self._addresses) <= 0:
            raise RuntimeWarning("Can't encrypt empty wallet.")
        if self._locked:
            raise RuntimeWarning("Can't encrypt locked down wallet.")
        if self._infos['encrypted']:
            # TODO
            raise RuntimeWarning("TODO: decrypt and re-encrypt - WIP")
        encrypted_addresses = []
        for address in self._addresses:
            content = json.dumps(address)
            encrypted_addresses.append(b64encode(encrypt(password, content)).decode('utf-8'))
        self._data['addresses'] = encrypted_addresses
        self._data['encrypted'] = True
        self.save()
        self._master_password = password
        self._infos['encrypted'] = True
        self._locked = False

    def lock(self):
        """Lock the wallet"""
        self._master_password = ''      # forget the pass
        self._locked = self._data['encrypted']
        if self._locked:
            # If wallet was encrypted, then forget the addresses also.
            self._addresses = []

    def unlock(self, password:str):
        """Sets the master password and unlocks the wallet"""
        if not self._locked:
            return
        if not self._infos['encrypted']:
            return
        # decrypt the addresses and keys
        try:
            addresses = []
            for address in self._data['addresses']:
                decoded = json.loads(decrypt(password, b64decode(address.encode('utf-8'))).decode('utf-8'))
                addresses.append(decoded)
            self._addresses = addresses
            self._master_password = password
            self._locked = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            raise RuntimeWarning("Password does not seem to match")

    def new(self, wallet_file='wallet.der'):
        """
        Creates a new wallet - only if the given file does not exist yet.
        Does not load it.

        :param wallet_file: string, a wallet file path
        :return True or False depending on the op success
        """
        raise RuntimeWarning("Not to be used in multi context")
        """
        if self.verbose:
            print("create", wallet_file)
        if path.isfile(wallet_file):
            if self.verbose:
                print("{} Already exists, canceled".format(wallet_file))
            return False
        bismuthcrypto.keys_new(wallet_file)
        return True
        """

    def new_address(self, label: str='', password: str='', salt: str=''):
        """
        Add a new address to the wallet (and save it)
        """
        if self._infos['encrypted'] and self._locked:
            raise RuntimeError("Wallet must be unlocked")
        keys = bismuthcrypto.keys_gen(password=password, salt=salt)
        keys['label'] = label
        keys['timestamp'] = int(time())
        self._addresses.append(keys)
        if self._infos['encrypted']:
            content = json.dumps(keys)
            encrypted = b64encode(encrypt(self._master_password, content)).decode('utf-8')
            self._data['addresses'].append(encrypted)
        else:
            print('1')
            self._data['addresses'].append(keys)
        self.save()

    def get_der_key(self, wallet_file: str='wallet.der', password: str=''):
        try:
            with open(wallet_file, 'r') as f:
                content = json.load(f)
                address = content['Address']  # Warning case change!!!
                if password:
                    content['Private Key'] = decrypt(password,b64decode(content['Private Key']))

                key = RSA.importKey(content['Private Key'])
                public_key = content['Public Key']
                private_key = content['Private Key']
                address = content("Address")
                # TODO: check that address matches rebuilded pubkey
                return {"private_key": private_key, "public_key": public_key, "address": address, "label":'',
                        'timestamp': int(time())}
        except:
            # encrypted
            return None

    def import_der(self, wallet_der: str='wallet.der', label: str='', source_password: str=''):
        """Import an existing wallet.der like file into the wallet"""
        if self._infos['encrypted'] and self._locked:
            # TODO: check could be done via a decorator
            raise RuntimeError("Wallet must be unlocked")
        key = self.get_der_key(wallet_der, password=source_password)
        if not key:
            raise RuntimeWarning("Error importing the der file")
        key['label'] = label
        self._addresses.append(key)
        if self._infos['encrypted']:
            content = json.dumps(key)
            encrypted = b64encode(encrypt(self._master_password, content)).decode('utf-8')
            self._data['addresses'].append(encrypted)
        else:
            print('1')
            self._data['addresses'].append(key)
        self.save()

    @property
    def address(self):
        """Returns the currently loaded address, or None"""
        return self._address
