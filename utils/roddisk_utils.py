import numpy as np

# Define some needed functions
def specialRound(number):
    numberOfDecimals = str(number)[::-1].find('.')
    if numberOfDecimals <= 2:
        return number
    else:
        return "{:.2f}".format(number)
