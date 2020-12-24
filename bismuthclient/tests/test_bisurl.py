import sys

sys.path.append('../')
from bismuthclient.bismuthutil import BismuthUtil


def test_encode_bis_url_legacy(verbose=False):
    recipient = "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    amount = "1.234"
    operation = ""
    openfield = ""
    bis_url = BismuthUtil.create_bis_url(recipient, amount, operation, openfield, legacy=True)
    assert bis_url == "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234///Bg#w)r%}J-4Ct__J|z#_"
    recipient = "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    amount = "1.234"
    operation = "token:transfer"
    openfield = "test:1"
    bis_url = BismuthUtil.create_bis_url(recipient, amount, operation, openfield, legacy=True)
    assert bis_url == "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234/bZ={AZaQ>wVQzC~WpV/bY*jNIxz/>H!cQZ*|L=^XYba0XP&1"
    recipient = "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    amount = "1.234"
    operation = "token:transfer"
    openfield = 'test:1:{"Message":"Test message"}'
    bis_url = BismuthUtil.create_bis_url(recipient, amount, operation, openfield, legacy=True)
    assert bis_url == "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234/bZ={AZaQ>wVQzC~WpV/bY*jNIx#wXB28s;b75y?B03^eWpi{OZDn(FVP|C`eE/#04XIp(|p18$+t~x+8E0"


def test_encode_bis_url_new(verbose=False):
    recipient = "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    amount = "1.234"
    operation = ""
    openfield = ""
    bis_url = BismuthUtil.create_bis_url(recipient, amount, operation, openfield, legacy=False)
    assert bis_url == "bis://8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234///g2ietw=="
    recipient = "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    amount = "1.234"
    operation = "token:transfer"
    openfield = "test:1"
    bis_url = BismuthUtil.create_bis_url(recipient, amount, operation, openfield, legacy=False)
    assert bis_url == "bis://8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234/dG9rZW46dHJhbnNmZXI=/dGVzdDox/ldW-ig=="
    recipient = "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    amount = "1.234"
    operation = "token:transfer"
    openfield = 'test:1:{"Message":"Test message"}'
    bis_url = BismuthUtil.create_bis_url(recipient, amount, operation, openfield, legacy=True)
    assert bis_url == "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234/bZ={AZaQ>wVQzC~WpV/bY*jNIx#wXB28s;b75y?B03^eWpi{OZDn(FVP|C`eE/#04XIp(|p18$+t~x+8E0"


def test_decode_bis_url_legacy(verbose=False):
    bis_url = "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234///Bg#w)r%}J-4Ct__J|z#_"
    decoded = BismuthUtil.read_url(bis_url, legacy=True)
    if verbose:
        print(decoded)
    assert decoded['recipient'] == "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    assert decoded['amount'] == "1.234"
    assert decoded['operation'] == ""
    assert decoded['openfield'] == ""
    bis_url = "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234/bZ={AZaQ>wVQzC~WpV/bY*jNIxz/>H!cQZ*|L=^XYba0XP&1"
    decoded = BismuthUtil.read_url(bis_url, legacy=True)
    assert decoded['recipient'] == "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    assert decoded['amount'] == "1.234"
    assert decoded['operation'] == "token:transfer"
    assert decoded['openfield'] == "test:1"
    # Now test a broken hash
    bis_url = "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234///Ag#w)r%}J-4Ct__J|z#_"
    decoded = BismuthUtil.read_url(bis_url, legacy=True)
    if verbose:
        print(decoded)
    assert "Error" in decoded
    bis_url = "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234/bZ={AZaQ>wVQzC~WpV/bY*jNIx#wXB28s;b75y?B03^eWpi{OZDn(FVP|C`eE/#04XIp(|p18$+t~x+8E0"
    decoded = BismuthUtil.read_url(bis_url, legacy=True)
    assert decoded['recipient'] == "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    assert decoded['amount'] == "1.234"
    assert decoded['operation'] == "token:transfer"
    assert decoded['openfield'] == 'test:1:{"Message":"Test message"}'


def test_decode_bis_url_new(verbose=False):
    bis_url = "bis://8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234///g2ietw=="
    decoded = BismuthUtil.read_url(bis_url, legacy=False)
    if verbose:
        print("new", decoded)
    assert decoded['recipient'] == "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    assert decoded['amount'] == "1.234"
    assert decoded['operation'] == ""
    assert decoded['openfield'] == ""
    bis_url = "bis://8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234/dG9rZW46dHJhbnNmZXI=/dGVzdDox/ldW-ig=="
    decoded = BismuthUtil.read_url(bis_url, legacy=False)
    assert decoded['recipient'] == "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    assert decoded['amount'] == "1.234"
    assert decoded['operation'] == "token:transfer"
    assert decoded['openfield'] == "test:1"
    # Now test a broken hash
    bis_url = "bis://8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234///g4ietw=="
    decoded = BismuthUtil.read_url(bis_url, legacy=False)
    if verbose:
        print("new", decoded)
    assert "Error" in decoded
    bis_url = "bis://pay/8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742/1.234/bZ={AZaQ>wVQzC~WpV/bY*jNIx#wXB28s;b75y?B03^eWpi{OZDn(FVP|C`eE/#04XIp(|p18$+t~x+8E0"
    decoded = BismuthUtil.read_url(bis_url, legacy=True)
    assert decoded['recipient'] == "8342c1610de5d7aa026ca7ae6d21bd99b1b3a4654701751891f08742"
    assert decoded['amount'] == "1.234"
    assert decoded['operation'] == "token:transfer"
    assert decoded['openfield'] == 'test:1:{"Message":"Test message"}'


if __name__ == "__main__":
    test_encode_bis_url_legacy(True)
    test_encode_bis_url_new(True)
    test_decode_bis_url_legacy(True)
    test_decode_bis_url_new(True)
