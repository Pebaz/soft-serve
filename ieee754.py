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
        # TODO(pbz): Fix indexing: self[9:] failed
        return self[9:len(self)]

    def __add__(self, other: 'Single'):
        is_zero = not self.exponent()
        return self

    def bytes(self, byte_order: Optional[Order] = None) -> bytes:
        # TODO(pbz): Tidbytes to big_endian_bytes or little_endian_bytes
        byte_order = byte_order or (L2R, R2L)[sys.byteorder == 'big']
        it = self.rgn.bytes if byte_order == L2R else reversed(self.rgn.bytes)
        buffer = b''

        for byte in it:
            acc = 0
            for i, bit in enumerate(reversed(byte)):
                # TODO(pbz): Implement this nifty multiply trick in tidbytes
                acc |= (1 << i) * bit
            buffer += bytes([acc])
        return buffer

    def __float__(self):
        return struct.unpack('f', self.bytes())[0]

    def __str__(self):
        return str(float(self))


single1 = Single('10000000')
single2 = Single('0')
# print(single1 + single2)
print(Mem(single1.bytes()))
print(repr(single1))
print(single1.bytes())
print(float(single1))
print(single1)
# TODO(pbz): Fix from_float in tidbytes to suggest using f32 (currently doesn't)
print(Single(f32(3.14)))
print(int(single1))