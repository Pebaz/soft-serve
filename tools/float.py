"""
A couple goals:

1. Take string in, convert to binary float (for a compiler)
2. Take binary float in, convert to string (for a program)
"""

# 0. https://github.com/grzegorz-kraszewski/stringtofloat/blob/master/str2dbl.c <AND> http://krashan.ppa.pl/articles/stringtofloat/
# 1. https://github.com/gcc-mirror/gcc/blob/master/libgcc/soft-fp/single.h
# 2. https://class.ece.iastate.edu/arun/CprE281_F05/ieee754/ie5.html
# 3. https://gcc.gnu.org/onlinedocs/gccint/Soft-float-library-routines.html

class BitArray:
    def __init__(self, width):
        self.bits = [0] * width

    def __getitem__(self, index):
        return self.bits[index]

    def __setitem__(self, index, value):
        assert index in range(len(self.bits))
        self.bits[len(self.bits) - 1 - index] = value

    def __str__(self):
        return ''.join(str(i) for i in self.bits)

    def __repr__(self):
        return str(self)

    def __format__(self, *args):
        return str(self)


a = BitArray(32)
print(a)
a[31] = 1
print(a)


# Python program to convert a real value
# to IEEE 754 Floating Point Representation.

# Function to convert a
# fraction to binary form.
def binaryOfFraction(fraction):

    # Declaring an empty string
    # to store binary bits.
    binary = str()

    # Iterating through
    # fraction until it
    # becomes Zero.
    while (fraction):

        # Multiplying fraction by 2.
        fraction *= 2

        # Storing Integer Part of
        # Fraction in int_part.
        if (fraction >= 1):
            int_part = 1
            fraction -= 1
        else:
            int_part = 0

        # Adding int_part to binary
        # after every iteration.
        binary += str(int_part)

    # Returning the binary string.
    return binary

# Function to get sign  bit,
# exp bits and mantissa bits,
# from given real no.
def floatingPoint(real_no):

    # Setting Sign bit
    # default to zero.
    sign_bit = 0

    # Sign bit will set to
    # 1 for negative no.
    if(real_no < 0):
        sign_bit = 1

    # converting given no. to
    # absolute value as we have
    # already set the sign bit.
    real_no = abs(real_no)

    # Converting Integer Part
    # of Real no to Binary
    int_str = bin(int(real_no))[2 : ]

    # Function call to convert
    # Fraction part of real no
    # to Binary.
    fraction_str = binaryOfFraction(real_no - int(real_no))

    # Getting the index where
    # Bit was high for the first
    # Time in binary repres
    # of Integer part of real no.
    ind = int_str.index('1')

    # The Exponent is the no.
    # By which we have right
    # Shifted the decimal and
    # it is given below.
    # Also converting it to bias
    # exp by adding 127.
    exp_str = bin((len(int_str) - ind - 1) + 127)[2 : ]

    # getting mantissa string
    # By adding int_str and fraction_str.
    # the zeroes in MSB of int_str
    # have no significance so they
    # are ignored by slicing.
    mant_str = int_str[ind + 1 : ] + fraction_str

    # Adding Zeroes in LSB of
    # mantissa string so as to make
    # it's length of 23 bits.
    mant_str = mant_str + ('0' * (23 - len(mant_str)))

    # Returning the sign, Exp
    # and Mantissa Bit strings.
    return sign_bit, exp_str, mant_str

# Driver Code
if __name__ == "__main__":

    # Function call to get
    # Sign, Exponent and
    # Mantissa Bit Strings.
    num = -2.205 / 0.1
    sign_bit, exp_str, mant_str = floatingPoint(num)

    # Final Floating point Representation.
    ieee_32 = str(sign_bit) + '|' + exp_str + '|' + mant_str

    # Printing the ieee 32 representation.
    print(f"IEEE 754 representation of {num} is :")
    print(ieee_32)


print()


# Python program to convert
# IEEE 754 floating point representation
# into real value

# Function to convert Binary
# of Mantissa to float value.
def convertToInt(mantissa_str):

    # variable to make a count
    # of negative power of 2.
    power_count = -1

    # variable to store
    # float value of mantissa.
    mantissa_int = 0

    # Iterations through binary
    # Number. Standard form of
    # Mantissa is 1.M so we have
    # 0.M therefore we are taking
    # negative powers on 2 for
    # conversion.
    for i in mantissa_str:
        print(2, power_count)

        # Adding converted value of
        # Binary bits in every
        # iteration to float mantissa.
        mantissa_int += (int(i) * pow(2, power_count))

        # count will decrease by 1
        # as we move toward right.
        power_count -= 1

    print(mantissa_int, type(mantissa_int))

    # returning mantissa in 1.M form.
    return (mantissa_int + 1)

if __name__ == "__main__":
    # Floating Point Representation
    # to be converted into real
    # value.
    # ieee_32 = '1|10000000|00100000000000000000000'

    # First bit will be sign bit.
    sign_bit = int(ieee_32[0])

    # Next 8 bits will be
    # Exponent Bits in Biased
    # form.
    exponent_bias = int(ieee_32[2 : 10], 2)

    # In 32 Bit format bias
    # value is 127 so to have
    # unbiased exponent
    # subtract 127.
    exponent_unbias = exponent_bias - 127

    # Next 23 Bits will be
    # Mantissa (1.M format)
    mantissa_str = ieee_32[11 : ]

    # Function call to convert
    # 23 binary bits into
    # 1.M real no. form
    mantissa_int = convertToInt(mantissa_str)

    # The final real no. obtained
    # by sign bit, mantissa and
    # Exponent.
    real_no = pow(-1, sign_bit) * mantissa_int * pow(2, exponent_unbias)

    # Printing the obtained
    # Real value of floating
    # Point Representation.
    print("The float value of the given IEEE-754 representation is :",real_no)
