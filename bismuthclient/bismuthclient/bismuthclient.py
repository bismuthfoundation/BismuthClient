"""
A all in one Bismuth Native client that connects to local or distant wallet servers
"""

# import json
import logging

# from bismuthclient import async_client
from bismuthclient import bismuthapi
from bismuthclient.bismuthwallet import BismuthWallet
from bismuthclient import rpcconnections
from bismuthclient import lwbench
from bismuthclient.bismuthformat import TxFormatter, AmountFormatter
from os import path, scandir

__version__ = '0.0.3'


class BismuthClient():

    __slots__ = ('initial_servers_list', 'servers_list', 'app_log', '_loop', 'address', '_current_server',
                 'wallet_file', '_wallet', '_connection', 'verbose')

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
            transactions = self.command("addlistlim", [self.address, num])
        except:
            # TODO: Handle retry, at least error message.
            transactions = []

        #json = [dict(zip(["block_height", "timestamp", "address", "recipient", "amount", "signature", "public_key", "block_hash", "fee", "reward", "operation", "openfield"], tx)) for tx in transactions]
        json = [TxFormatter(tx).to_json(for_display=for_display) for tx in transactions]
        return json

    def balance(self, for_display=False):
        """
        Returns the current balance for the current address.
        """
        if not self.address or not self._wallet:
            return []
        try:
            balance = self.command("balanceget", [self.address])
            balance = balance[0]
        except:
            # TODO: Handle retry, at least error message.
            balance = 'N/A'
        if for_display:
            balance = AmountFormatter(balance).to_string(leading=0)
        return balance

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
        self.address = self._wallet.address

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
        self.servers_list = bismuthapi.get_wallet_servers_legacy(self.initial_servers_list, self.app_log)
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
        return self._connection.command(command, options)
