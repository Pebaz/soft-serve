import struct, sys
from typing import Optional
from tidbytes import Mem, Unsigned, f32, Order, L2R, R2L

# TODO(pbz): Float to string algorithm: RYU: https://github.com/ulfjack/ryu

class Double(Mem[64]): ...
class Single(Mem[32]):
    def sign(self) -> 'Unsigned[1]':
        return self[0]

    def exponent(self) -> Unsigned[8]:
        return self[1:9]

    def mantissa(self) -> Unsigned[23]:
        return self[9:]

    def __add__(self, other: 'Single'):
        is_zero = not self.exponent()
        return self

    def __float__(self):
        "struct.unpack and Single.bytes assume system endianness by default."
        return struct.unpack('f', self.bytes())[0]

    def __str__(self):
        return str(float(self))


single1 = Single('10000000')
single2 = Single('0')
# print(single1 + single2)
print(Single(f32(3.14)))
