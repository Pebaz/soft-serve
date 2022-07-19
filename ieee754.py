"""
Float Toy: https://evanw.github.io/float-toy/
Best Addition Video: https://www.youtube.com/watch?v=mKJiD2ZAlwM
"""

# Exponent - 127

# Shift smaller mantissa by bigger exponent - smaller exponent

# Then directly add both numbers

import struct

def f32_to_bits(f32: float) -> int:
    # * Losing precision here ('!i') since Python's f32 is actually f64
    return struct.unpack('!I', struct.pack('!f', f32))[0]

def bits_to_f32(bits: int) -> float:
    try:
        as_int = struct.pack('!I', bits)
        return struct.unpack('!f', as_int)[0]
    except:
        import ipdb; ipdb.set_trace()

assert bits_to_f32(f32_to_bits(3.14)) == 3.140000104904175

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

    def combine(self, other):
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

def int_to_bit_width(num, bit_width):
    bits = [int(i) for i in bin(num)[2:]]
    bits = ([0] * (bit_width - len(bits))) + bits
    return bits

class Float32(Bits[32]):
    def __init__(self, initializer):
        if isinstance(initializer, float):
            float_memory = f32_to_bits(initializer)
            super().__init__(int_to_bit_width(float_memory, self.bit_width))
        elif isinstance(initializer, str):
            super().__init__(bin_to_bits(initializer))
        else:
            raise NotImplementedError('Unsupported initializer type')

    __str__ = lambda self: str(float(self))

    def __repr__(self):
        s = self.sign()[0]
        e = str(self.exponent())
        m = str(self.mantissa())
        return f'<{self.__class__} {float(self)} s={s:b} e={e} m={m}>'

    sign = lambda self: self[:1]
    exponent = lambda self: self[1:9]
    mantissa = lambda self: self[9:]

    def __add__(self, other):
        assert type(self) is type(other), (
            f'Incompatible types: cannot add {type(other)} to {type(self)}'
        )

        self_sign = self.sign()
        other_sign = other.sign()
        self_mantissa = self.mantissa()
        other_mantissa = other.mantissa()
        self_exponent = int(self.exponent()) - 127
        other_exponent = int(other.exponent()) - 127

        print('Mantissa:'.ljust(13), self_mantissa, other_mantissa)
        print('Exponent:'.ljust(13), self_exponent, other_exponent)

        # TODO(pbz): Use this to know when to add the 1
        is_zero = int(self.exponent()) == 0
        if is_zero:
            "Don't add the implicit 1 to the mantissa"

        # Add implicit 1 for normalized form
        # ! CRITICAL
        # TODO(pbz): Shifting would imply losing some information
        # TODO(pbz): Is it ok to just add the bit since this would most likely
        # TODO(pbz): Be within an i32 in C code anyway (Enough room)?
        self_mantissa = Bits[1]([1]).combine(self_mantissa)
        other_mantissa = Bits[1]([1]).combine(other_mantissa)

        print('Mantissa:'.ljust(13), self_mantissa, other_mantissa)
        print('Exponent:'.ljust(13), self_exponent, other_exponent)

        if self_exponent < other_exponent:
            # Shift by difference to make both exponents now match
            self_mantissa >> other_exponent - self_exponent
            self_exponent = other_exponent

        elif self_exponent > other_exponent:
            # Shift by difference to make both exponents now match
            other_mantissa >> self_exponent - other_exponent
            other_exponent = self_exponent

        print('Mantissa:'.ljust(13), self_mantissa, other_mantissa)
        print('Exponent:'.ljust(13), self_exponent, other_exponent)

        # * This new method is just using hardware int addition on the mantssas!
        # new_mantissa = self_mantissa + other_mantissa
        new_mantissa = Bits[len(self_mantissa.bits)](
            int_to_bit_width(
                int(self_mantissa) + int(other_mantissa),
                len(self_mantissa.bits)
            )
        )
        print('New Mantissa:', new_mantissa)

        # ! CRITICAL
        # TODO(pbz): Shifting off the implicit normalized form 1 bit
        new_mantissa = new_mantissa << 1
        new_mantissa = new_mantissa[:-1]

        print('New Mantissa:', new_mantissa)

        print('1.' + str(new_mantissa[:-16]) + ' * 2 ** ' + str(self_exponent))

        new_exponent = self_exponent + 127
        print('New Exponent:', new_exponent)
        new_exponent = Bits[8](int_to_bit_width(new_exponent, 8))
        print('New Exponent:', new_exponent)

        # TODO(pbz): Have to assume sign is positive until I figure it out
        new_sign = Bits[1]([0])

        result = new_sign.combine(new_exponent.combine(new_mantissa))

        print('Result:', result)

        float_result = Float32('0' * self.bit_width)
        float_result.bits = result.bits
        return float_result

    def __float__(self):
        def set_bit(value, bit):
            return value | (1 << bit)

        def clear_bit(value, bit):
            return value & ~(1 << bit)

        result = 0

        for bit_index, bit in enumerate(reversed(self.bits)):
            if bit:
                result = set_bit(result, bit_index)

        return bits_to_f32(result)

assert float(Float32(3.14)) == 3.140000104904175, (
    'Python floats are actually 64 bit so they can store 3.14 precisely. If you'
    'do: ctypes.c_float(3.14), it also prints: 3.140000104904175.'
)

def bin_to_bits(binary_literal_string):
    return [int(i) for i in binary_literal_string]

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

print()

x = Float32('01000010000011110000000000000000')
y = Float32('01000001101001000000000000000000')
result = x + y
assert float(result) == 56.25
print(result)
print('\n  Float:', float(result))
print('\n  Float:', struct.unpack('!f', 0b01000010011000010000000000000000.to_bytes(4, 'big')))

print()
print(float(Float32(3.14)))
print()

print('.>', f32_to_bits(3.14))
print('.>', bits_to_f32(1078523331))
print()

negative_pi = Float32('11000000010010010000111111011011')
print('negative_pi  =', negative_pi)
one_point_oh = Float32(1.0)
print('one_point_oh = ', one_point_oh)
# TODO(pbz): Make negative addition work in fixed point first
# ! print(one_point_oh + negative_pi)
