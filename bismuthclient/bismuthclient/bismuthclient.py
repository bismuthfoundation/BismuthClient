"""
A all in one Bismuth Native client that connects to local or distant wallet servers
"""

import base64
# import json
import logging
import time
import sys
import os

# from bismuthclient import async_client
from bismuthclient import bismuthapi
from bismuthclient.bismuthwallet import BismuthWallet
from bismuthclient import bismuthcrypto
from bismuthclient import rpcconnections
from bismuthclient import lwbench
from bismuthclient.bismuthformat import TxFormatter, AmountFormatter
from os import path, scandir

__version__ = '0.0.44'


class BismuthClient():

    __slots__ = ('initial_servers_list', 'servers_list', 'app_log', '_loop', 'address', '_current_server',
                 'wallet_file', '_wallet', '_connection', '_cache', 'verbose')

    def __init__(self, servers_list=None, app_log=None, loop=None, wallet_file='', verbose=False):
        """
        Init the main class.

        :param servers_list: list of "ip:port" wallet servers
        :param app_log:
        :param loop: None of an asyncio loop
        :param address:
        """
        self.verbose = verbose
        if not servers_list:
            servers_list = []
        self.initial_servers_list = servers_list
        if app_log:
            self.app_log = app_log
        elif logging.getLogger("tornado.application"):
            self.app_log = logging.getLogger("tornado.application")
        else:
            self.app_log = logging
        self._loop = loop
        self.wallet_file = None
        self._wallet = None
        self.address = None
        self.load_wallet(wallet_file)
        self.servers_list = servers_list
        self._current_server = None
        self._connection = None
        self._cache = {}

    def _get_cached(self, key, timeout_sec=30):
        if key in self._cache:
            data = self._cache[key]
            if data[0] + timeout_sec >= time.time():
                """                
                if self.verbose:
                    self.app_log.info("Cache Hit on {}".format(key))
                    # print(data[1])
                """
                return data[1]
        return None

    def _set_cache(self, key, value):
        self._cache[key] = (time.time(), value)

    def clear_cache(self):
        self._cache = {}

    @property
    def current_server(self):
        return self._current_server

    def list_wallets(self, scan_dir='wallets'):
        """
        Returns a list of dict for each wallet file found in the dir to scan.

        Each dict has the following keys: 'file', 'address', 'encrypted'

        :param scan_dir: string, the dir to scan for wallet (*.der files).
        """
        wallets = []
        for entry in scandir(scan_dir):
            print(entry)
            if entry.name.endswith('.der') and entry.is_file():
                 wallets.append(self._wallet.wallet_preview(entry.path))
        # TODO: sorts by name
        return wallets

    def latest_transactions(self, num=10, for_display=False):
        """
        Returns the list of the latest num transactions for the current address.

        Each transaction is a dict with the following keys:
        `["block_height", "timestamp", "address", "recipient", "amount", "signature", "public_key", "block_hash", "fee", "reward", "operation", "openfield"]`
        """
        if not self.address or not self._wallet:
            return []
        try:
            key = "tx{}".format(num)
            cached = self._get_cached(key)
            if cached:
                return cached
            transactions = self.command("addlistlim", [self.address, num])
        except:
            # TODO: Handle retry, at least error message.
            transactions = []

        #json = [dict(zip(["block_height", "timestamp", "address", "recipient", "amount", "signature", "public_key", "block_hash", "fee", "reward", "operation", "openfield"], tx)) for tx in transactions]
        json = [TxFormatter(tx).to_json(for_display=for_display) for tx in transactions]
        self._set_cache(key, json)
        return json

    def balance(self, for_display=False):
        """
        Returns the current balance for the current address.
        """
        if not self.address or not self._wallet:
            return 'N/A'
        try:
            cached = self._get_cached('balance')
            if cached:
                return cached
            balance = self.command("balanceget", [self.address])
            balance = balance[0]
            self._set_cache('balance', balance)
        except:
            # TODO: Handle retry, at least error message.
            balance = 'N/A'
        if for_display:
            balance = AmountFormatter(balance).to_string(leading=0)
        return balance

    def send(self, recipient: str, amount: float, operation: str='', data: str=''):
        """
        Sends the given tx
        """
        try:
            timestamp = time.time()
            public_key_hashed = base64.b64encode(self._wallet.public_key.encode('utf-8'))
            signature_enc = bismuthcrypto.sign_with_key(timestamp, self.address, recipient, amount, operation, data, self._wallet.key)
            txid = signature_enc[:56]
            tx_submit = ( '%.2f' % timestamp, self.address, recipient, '%.8f' % float(amount),
                          str(signature_enc), str(public_key_hashed.decode("utf-8")), operation, data)
            reply = self.command('mpinsert', [tx_submit])
            if self.verbose:
                print("Server replied '{}'".format(reply))
            if reply[-1] != "Success":
                print("Error '{}'".format(reply))
                return None
            if not reply:
                print("Server timeout")
                return None
            return txid
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def status(self):
        """
        Returns the current status of the wallet server
        """
        try:
            cached = self._get_cached('status')
            if cached:
                return cached
            status = self.command("statusjson")
            try:
                status['extended'] = self.command("wstatusget")
            except:
                status['extended'] = None
            self._set_cache('status', status)
        except:
            # TODO: Handle retry, at least error message.
            status = {}
        return status

    def load_wallet(self, wallet_file='wallet.der'):
        """
        Tries to load the wallet file

        :param wallet_file: string, a wallet.der file
        """
        # Default values, fail
        self.wallet_file = None
        self.address = None
        self._wallet = None
        self._wallet = BismuthWallet(wallet_file, verbose=self.verbose)
        self.wallet_file = wallet_file
        if self.address != self._wallet.address:
            self.clear_cache()
        self.address = self._wallet.address

    def new_wallet(self, wallet_file='wallet.der'):
        """
        Creates a new wallet if it does not already exists

        :param wallet_file: string, a wallet.der file
        """
        # Default values, fail
        wallet = BismuthWallet(wallet_file, verbose=self.verbose)
        return wallet.new(wallet_file)


    def wallet(self, full=False):
        """
        returns info about the currently loaded wallet

        if full is True, also force a check of the current balance.
        """
        return self._wallet.info()

    def info(self):
        """
        returns a dict with server info: ip, port, latest server status
        """
        connected = False
        if self._connection:
            connected = bool(self._connection.sdef)
        info = {"wallet": self.wallet_file, "address": self.address, "server": self._current_server, "servers_list": self.servers_list, "connected": connected}
        return info

    def get_server(self):
        """
        Tries to find the best available server given the config and sets self._current_server for later use.

        Returns the first connectible server.
        """
        # Use the API or bench to get the best one.
        self.servers_list = bismuthapi.get_wallet_servers_legacy(self.initial_servers_list, self.app_log, minver='0.1.5')
        # Now try to connect
        if self.verbose:
            print("self.servers_list", self.servers_list)
        for server in self.servers_list:
            if self.verbose:
                print("test server", server)
            if lwbench.connectible(server):
                self._current_server = server
                # TODO: if self._loop, use async version
                if self.verbose:
                    print("connect server", server)
                self._connection = rpcconnections.Connection(server, verbose=self.verbose)
                return server
        self._current_server = None
        self._connection = None
        # TODO: raise
        return None

    def command(self, command, options=None):
        """
        Makes sure we have a connection, runs a command and sends back the result.

        :param command: the command as a string
        :param options: optional options to the command, as a list if needed
        :return: the result as a native structure
        """
        if not self._current_server:
            # TODO: failsafe if can't connect
            self.get_server()
        if self.verbose:
            print("command {}, {}".format(command, options))
        return self._connection.command(command, options)
