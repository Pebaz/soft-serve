# Using float arithmetic, parse a string containing a floating point number.

number = input('Enter a floating point number: ')

try:
    result = float(number)
    print('You entered:', result)

except:
    print('Parse error:', number)
