


# def string_to_decimal(dec):
#     integer, fraction = dec.split('.')
#     bin_int = 0
#     half = int(integer)
#     rem = 0
#     count = 0

#     while half:
#         print(half)
#         count += 1
#         rem = half % 2
#         half = half // 2
#         bin_int |= 1 << count

#     return bin_int



# def decimal_to_float(): pass


# x = string_to_decimal('2.05')
# print(x, bin(x))



class BitArray:
    def __init__(self, width):
        self.bits = [0] * width

    def __getitem__(self, index):
        return self.bits[index]

    def __setitem__(self, index, value):
        self.bits[len(self.bits) - 1 - index] = value

    def __str__(self):
        return ''.join(str(i) for i in self.bits)

    def __repr__(self):
        return str(self)

    def __format__(self, *args):
        return str(self)


a = BitArray(8)
print(a)
a[0] = 1
print(a)

