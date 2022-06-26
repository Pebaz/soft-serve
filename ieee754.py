
# Exponent - 127

# Shift smaller mantissa by bigger exponent - smaller exponent

# Then directly add both numbers

import struct

class VariableBitWidth(type):
    registered_types, instantiated_types = {}, {}

    def __new__(cls, name, bases, dict_):
        cls.registered_types[name] = bases, dict_
        return super().__new__(cls, name, bases, dict_)

    def __getitem__(self, bit_width):
        class_object = self.instantiated_types.setdefault(
            f'{self.__name__}{bit_width}',
            super().__new__(
                self.__class__,
                self.__name__,
                *self.registered_types[self.__name__]
            )
        )

        class_object.bit_width = bit_width

        return class_object

    __str__ = lambda self: f'{self.__name__}{self.bit_width or "Abstract"}'
    __repr__ = __str__
    __format__ = lambda self, fmt: str(self)

class Bits(metaclass=VariableBitWidth):
    """
    ! Bits is data. Bits acts like a list of bits, reading from left to right.
    ! Treating this list of data as a number is entirely up to the user and the
    ! API treats the bit index zero as the leftmost bit in the bit region. This
    ! is consistent with other indexible data structures in Python.
    """
    bit_width = 0

    def __init__(self, bits: list[int] = None):
        self.bits = bits or [0] * self.bit_width
        assert len(self.bits) == self.bit_width, 'Invalid provided bit width'

    __str__ = lambda self: ''.join(str(i) for i in self.bits)
    __repr__ = lambda self: f'<{self.__class__} {self}>'
    __format__ = lambda self, _: str(self)

    def __getitem__(self, index):
        bits = self.bits[index]
        if isinstance(index, slice):
            return Bits[len(bits)](bits)
        else:
            return bits

    def __setitem__(self, index, value):
        self.bits[index] = value
        # TODO(pbz): Handle slice case

    def __add__(self, other):
        assert type(self) is type(other)
        carry = 0
        for i in reversed(range(self.bit_width)):
            # 💤 I know there's a better way but it's 2am on Friday
            self[i] = self[i] + other[i] + carry

            if self[i] > 2:
                self[i] = 1
                carry = 1
            elif self[i] > 1:
                self[i] = 0
                carry = 1
            else:
                carry = 0

        if carry:
            raise Exception('Addition Overflow')

        return self

    def __and__(self, other):
        bits = self.bits + other.bits
        return Bits[len(bits)](bits)

    def __int__(self):
        result = 0
        for bit in self.bits:
            result = result * 2 + bit
        return result

    def __lshift__(self, num_bits):
        for _ in range(num_bits):
            self.bits.pop(0)
            self.bits.append(0)
        return self

    def __rshift__(self, num_bits):
        for _ in range(num_bits):
            self.bits.pop(len(self.bits) - 1)
            self.bits.insert(0, 0)
        return self

assert Bits[0] is Bits[0]  # Type caching

# It doesn't make sense to have a Float class since mantissa can't be solved.
# Just make an indexible number class
class Float32(Bits[32]):
    def __init__(self, bit_string):
        super().__init__(bin_to_bits(bit_string))

    # def __init__(self, bits: list[int] = None):
    #     self.bits = bits or [0] * self.bit_width
    #     assert len(self.bits) == self.bit_width, 'Invalid provided bit width'

    __str__ = lambda self: ''.join(str(i) for i in self.bits)

    def __repr__(self):
        s = self.sign()[0]
        e = str(self.exponent())
        m = str(self.mantissa())
        return f'<{self.__class__} s={s:b} e={e} m={m}>'

    sign = lambda self: self[:1]
    exponent = lambda self: self[1:9]
    mantissa = lambda self: self[9:]

    def __add__(self, other):
        pass  # TODO(pbz): Override super().__add__()

        self_exponent = int(self.exponent()) - 127
        other_exponent = int(other.exponent()) - 127

        # ! Assume self_exponent larger for now

        print(self_exponent, other_exponent)



def bin_to_bits(binary_literal_string):
    return [int(i) for i in binary_literal_string]

def int_to_bit_width(num, bit_width):
    bits = [int(i) for i in bin(num)[2:]]
    bits = ([0] * (bit_width - len(bits))) + bits
    return bits

# ! This is wrong. Better way.
def float_to_bits(float_, is_double):
    bytes_ = struct.pack('d' if is_double else 'f', float_)
    for byte in reversed(bytes_):
        for bit_index in reversed(range(8)):
            bit = (byte >> bit_index) & 1
            print(bit, end='')
    print()

print(Bits)
print(Bits[4])
print(Bits[4]())
print(repr(Bits[4]()))
print()

a = Bits[8]()
a[0] = 1
print(a, repr(a))
print(a[:4], repr(a[:4]))
print(a[:4] + a[4:], repr(a[:4] + a[4:]))
print()

a = Bits[3]([0, 0, 1])
b = Bits[3]([0, 1, 1])
print('a =', a)
print('b =', b)
print('->', a + b)
print()

# https://www.youtube.com/watch?v=mKJiD2ZAlwM
print('\nAdd Two Float Numbers')
x = Bits[32](bin_to_bits('01000010000011110000000000000000'))
print('x =', x)
y = Bits[32](bin_to_bits('01000001101001000000000000000000'))
print('y =', y)
print()

xeb = x[1:9]
xe = int(xeb)
xm = x[9:]
yeb = y[1:9]
ye = int(yeb)
ym = y[9:]

print('xeb =', xeb, xe - 127)
print('yeb =', yeb, ye - 127)

print('xm =', xm)
print('ym =', ym)

# Make room for scientific notation bit
xm = xm >> 1
xm[0] = 1
ym = ym >> 1
ym[0] = 1
print('xm =', xm, 'with scientific bit set')
print('ym =', ym, 'with scientific bit set')

# Shift to match exponent
ym = ym >> xe - ye
print('xm =', xm)
print('ym =', ym, 'shifted', xe - ye, 'bits')

nm = xm + ym
print('nm =', nm)
print('gl = 11100001000000000000000')
print()

print(float_to_bits(3.14, False))
print('01000000010010001111010111000010')

print()

x = Float32('01000010000011110000000000000000')
y = Float32('01000001101001000000000000000000')
x + y