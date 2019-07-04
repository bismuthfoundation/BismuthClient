# BismuthClient and wallets

## Legacy wallet files

Legacy wallet app used single address wallets. These were wallet.der files.  
Despite the extension, that was a json file, holding b64encoded pem data.  

A single wallet contains
- a privkey
- a pubkey
- the matching address, derived from the pubkey

The privkey could optionally be encoded.  
Wallets were usually stored in the app directory.

**TODO: format spec and exemple**

## Multiwallets

Tornado Wallet introduced multiwallets: a single json file, wallet.json, with several sets of (privkey, pubkey, address).
Optionally encoded (all content, including address) with a single passphrase for all the sets.

This file is usually stored in a user private dir.

**TODO: format spec and exemple**

# Using a wallet with BismuthClient

- Create a BismuthClient instance  
`bismuthclient = BismuthClient(servers_list=None, app_log=None, loop=None, wallet_file='', verbose=False)`  
default behaviour is to use the single wallet scheme

- If you want a multiwallet, explicitely load it:  
`bismuthclient.load_multi_wallet(wallet_file='wallet.json')`

## Public Wallet methods

| method | single wallet | multi wallet | Comment
-----------------------------------------------------
|load_wallet(wallet_file='wallet.der') | Valid | Invalid | 
|load_multi_wallet(wallet_file='wallet.json') | Invalid | Valid |
|set_address(address: str='')| Invalid | Valid | Define active address of the multiwallet, address must exist in the multiwallet
|new_wallet(wallet_file='wallet.der') | Irrelevant | Irrelevant | Creates a new single wallet, does not load it. current wallet, single or multi, is unchanged
|wallet(full=False) | Valid | Valid | Info about the current (single or multi) wallet. If full is True, also force a check of the current balance

## Private wallet property and methods
