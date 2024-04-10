from tidbytes import Mem, Unsigned, u8

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

    def bytes(self):
        buffer = b''
        for byte in self.rgn.bytes:
            acc = 0
            for i, bit in enumerate(byte):
                if bit:
                    acc |= 1 << (8 - i)
            print(bin(acc))
            buffer += bytes([acc])
        return buffer

    def __float__(self):
        # TODO(pbz): Create to_bytes()
        pass

    def __str__(self):
        return str(float(self))


single1 = Single('1')
single2 = Single('0')
# print(single1 + single2)
print(single1.bytes())
