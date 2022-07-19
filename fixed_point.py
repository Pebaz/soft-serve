
from regex import B


def Fixed(width, dot):
    class FixedDecimal:
        def __init__(self, value):
            # TODO(pbz): If isinstance(...)
            self.value = value

        def __float__(self):
            b4_dot = ('0' * width) + bin(self.value)[2:]
            b4_dot = b4_dot[len(b4_dot) - dot:]
            dec = 0.0
            for i in range(dot):
                if b4_dot[i] == '1':
                    dec += 2 ** -(2 ** i)

            int_ = 0
            for i in range(dot, width):
                if self.value & (1 << i):
                    int_ += 2 ** (i - dot)

            return float(int_) + dec

        def __str__(self):
            if not dot:
                "It's just an integer at this point"
                return bin(self.value)[2:]
            buf = ''
            for i in range(width):
                bit = 0b1 << i
                buf = ('1' if self.value & bit else '0') + buf
                if i == dot - 1:
                    buf = '.' + buf
            return buf

        def __add__(self, other):
            self.value += other.value
            return self

    return FixedDecimal

Fix8 = Fixed(8, 4)

a = Fix8(0b00001000)
print(float(a), a)

b = Fix8(0b00000100)
print(float(b), b)

c = a + b
print(float(c), c)
