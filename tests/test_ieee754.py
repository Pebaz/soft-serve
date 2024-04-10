from ieee754 import *

def test_ieee754():
    single = Single()
    assert str(single.sign()) == '0'
    assert str(single.exponent()) == '00000000'
    assert str(single.mantissa()) == '00000000 00000000 0000000'

    single = Single('101')
    assert str(single.sign()) == '1'
    assert str(single.exponent()) == '01000000'
    assert str(single.mantissa()) == '00000000 00000000 0000000'

def test_addition():
    single = Single()
    single + single
