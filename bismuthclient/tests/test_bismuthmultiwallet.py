#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bismuthclient` package.


Warning: NEVER use the test addresses or seed, as they are public!
"""

import pytest
import sys
import os
import base64

sys.path.append('../')
from bismuthclient.bismuthmultiwallet import BismuthMultiWallet
from bismuthclient.bismuthcrypto import keys_gen


def test0_ainit():
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    try:
        os.remove("tmp/wallet1.json")
    except:
        pass
    try:
        os.remove("tmp/wallet2.json")
    except:
        pass
    try:
        os.remove("tmp/wallet3.json")
    except:
        pass
    try:
        os.remove("tmp/wallet_ed25519.json")
    except:
        pass


def test1_create_clear_multiwallet():
    wallet = BismuthMultiWallet("tmp/wallet1.json", seed="seed1")


def test2_add_address():
    wallet = BismuthMultiWallet("tmp/wallet1.json", seed="seed2")
    wallet.new_address(label="ad1", password="1", salt="1")
    # wallet.new_address(label="ad2", password="2", salt="1")


def test2b_read_address():
    wallet = BismuthMultiWallet("tmp/wallet1.json")
    assert wallet._addresses[0]['address'] == '59994eac4a36942fdbb05e33a353f72850f26112123840844bedb870'


def test3_create_empty_encrypted_multiwallet():
    wallet = BismuthMultiWallet("tmp/wallet2.json", seed="seed2")
    with pytest.raises(Exception) as e_info:
        wallet.encrypt("some_password", current_password=None)


def test4a_create_encrypted_multiwallet():
    wallet = BismuthMultiWallet("tmp/wallet3.json", seed="seed2")
    wallet.new_address(label="ad1", password="1", salt="1")  # Will auto save
    wallet.encrypt("some_password", current_password=None)  # Will auto save
    wallet.lock()
    wallet.unlock("some_password")
    assert wallet._addresses[0]['address'] == '59994eac4a36942fdbb05e33a353f72850f26112123840844bedb870'


def test4b_addto_encrypted_multiwallet():
    wallet = BismuthMultiWallet("tmp/wallet3.json")
    wallet.unlock("some_password")
    wallet.new_address(label="ad2", password="2", salt="2")  # Will auto save
    for address in wallet._addresses:
        print(address['address'])


def test5_ed25519_address_signing():
    wallet = BismuthMultiWallet("tmp/wallet_ed25519.json", seed="seed-ed25519")
    wallet.new_address(label="ed1", password="ed25519-password", salt="ed25519-salt", type="ED25519")
    address = wallet._addresses[0]['address']
    assert address.startswith('Bis')
    assert wallet._addresses[0]['type'] == 'ED25519'

    wallet.set_address(address)
    pubkey = wallet.get_encoded_pubkey()
    assert len(base64.b64decode(pubkey)) == 32

    signature = wallet.sign_encoded(1234567890.12, address, "bis-recipient", 1.25, "operation", "openfield")
    assert len(base64.b64decode(signature)) == 64


def test6_ecdsa_address_signing():
    wallet = BismuthMultiWallet("tmp/wallet_ecdsa.json", seed="seed-ecdsa")
    wallet.new_address(label="ecdsa1", password="ecdsa-password", salt="ecdsa-salt", type="ECDSA")
    address = wallet._addresses[0]['address']
    assert address
    assert wallet._addresses[0]['type'] == 'ECDSA'

    wallet.set_address(address)
    pubkey = wallet.get_encoded_pubkey()
    assert len(base64.b64decode(pubkey)) == 33

    signature = wallet.sign_encoded(1234567890.12, address, "bis-recipient", 1.25, "operation", "openfield")
    assert len(base64.b64decode(signature)) > 0


if __name__ == "__main__":
    # print(keys_gen('test', 'salt', verbose=True))
    test0_ainit()
    # test2_add_address()
    # test2b_read_address()
    test4a_create_encrypted_multiwallet()
    test4b_addto_encrypted_multiwallet()
