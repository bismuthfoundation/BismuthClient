import sys

sys.path.append('../')
from bismuthclient.bismuthutil import BismuthUtil


def test_sublimate1(verbose=False):
    res = BismuthUtil.sublimate("Test!", 3)
    if verbose:
        print(res)
    res2 = BismuthUtil.condensate(res['parts'])
    if verbose:
        print(res2)
    assert res2["key"] == "Test!"


def test_sublimate2(verbose=False):
    res = BismuthUtil.sublimate("Test of a longer string, that could be an ECDSA privkey for instance", 10)
    if verbose:
        print(res)
    res2 = BismuthUtil.condensate(res['parts'])
    if verbose:
        print(res2)
    assert res2["key"] == "Test of a longer string, that could be an ECDSA privkey for instance"


def test_condensate(verbose=False):
    res = {'count': 3, 'parts': [b'*yx\x1d\xd5', b'\x8d\xdb\xadB\xe9', b'\xf3\xc7\xa6+\x1d'], 'hash': '9382c22f'}
    res2 = BismuthUtil.condensate(res['parts'])
    if verbose:
        print(res2)
    assert res2["key"] == "Test!"
    assert res2["hash"] == '9382c22f'


if __name__ == "__main__":
    test_sublimate1(True)
    test_sublimate2(True)
    test_condensate(True)
