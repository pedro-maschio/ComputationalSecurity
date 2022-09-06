import pytest

from aes.aes import AES 


def test_shift_rows():
    a = AES()

    assert a.shift_rows([[0x8e, 0x9f, 0x01, 0xc6], [0x4d, 0xdc, 0x01, 0xc6], [0xa1, 0x58, 0x01, 0xc6], [0xbc, 0x9d, 0x01, 0xc6]]) == [[0x8e, 0x9f, 0x01, 0xc6], [0xdc, 0x01, 0xc6, 0x4d], [0x01, 0xc6, 0xa1, 0x58], [0xc6, 0xbc, 0x9d, 0x01]]
    
def test_inverse_shift_rows():
    a = AES()

    assert a.inverse_shift_rows([[0x8e, 0x9f, 0x01, 0xc6], [0xdc, 0x01, 0xc6, 0x4d], [0x01, 0xc6, 0xa1, 0x58], [0xc6, 0xbc, 0x9d, 0x01]]) == [[0x8e, 0x9f, 0x01, 0xc6], [0x4d, 0xdc, 0x01, 0xc6], [0xa1, 0x58, 0x01, 0xc6], [0xbc, 0x9d, 0x01, 0xc6]]
    