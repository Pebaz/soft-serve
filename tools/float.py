


def string_to_decimal(dec):
    integer, fraction = dec.split('.')
    bin_int = 0
    half = int(integer)
    rem = 0
    count = 0

    while half:
        print(half)
        count += 1
        rem = half % 2
        half = half // 2
        bin_int |= 1 << count

    return bin_int



def decimal_to_float(): pass


x = string_to_decimal('2.05')
print(x, bin(x))
