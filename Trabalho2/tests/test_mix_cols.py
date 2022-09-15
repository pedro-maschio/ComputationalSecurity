import pytest

from aes.aes import AES 

def test_mix_cols():
    a = AES()
    assert a.mix_cols([[0xdb, 0xf2, 0x01, 0xc6], [0x13, 0x0a, 0x01, 0xc6], [0x53, 0x22, 0x01, 0xc6], [0x45, 0x5c, 0x01, 0xc6]]) == [[0x8e, 0x9f, 0x01, 0xc6], [0x4d, 0xdc, 0x01, 0xc6], [0xa1, 0x58, 0x01, 0xc6], [0xbc, 0x9d, 0x01, 0xc6]]                                

def test_inverse_mix_cols():
    a = AES()
    assert a.inverse_mix_cols([[0x8e, 0x9f, 0x01, 0xc6], [0x4d, 0xdc, 0x01, 0xc6], [0xa1, 0x58, 0x01, 0xc6], [0xbc, 0x9d, 0x01, 0xc6]]) == [[0xdb, 0xf2, 0x01, 0xc6], [0x13, 0x0a, 0x01, 0xc6], [0x53, 0x22, 0x01, 0xc6], [0x45, 0x5c, 0x01, 0xc6]]                                