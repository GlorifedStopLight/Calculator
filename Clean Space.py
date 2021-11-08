

# takes in a number in string form returns the number of significant figures in the number (string)
def countSigFigs(number):

    # decimal is present
    decimalPresent = "." in number

    # this will be true when the loop has gone past the decimal
    pastedDecimal = False

    # remembers the number of significant figures
    significantFigures = 0

    # remember if we have iterated passed a non zero
    passedNonZero = False

    # loop through the number
    for index in range(len(number)):

        # index of number is a non zero
        if number[index] in "123456789":

            # we have passed a non zero
            passedNonZero = True

            # non zeros are always significant
            significantFigures += 1

        # at decimal point
        elif number[index] == ".":

            # loop has pasted the decimal point
            pastedDecimal = True

        # not pasted the decimal but there is a decimal present this index has to be a 0
        elif not pastedDecimal and decimalPresent == True and passedNonZero == True:

            # count this number as a significant figure
            significantFigures += 1

        # have pasted the decimal and passedNonZero
        elif pastedDecimal and passedNonZero:

            # zero is significant
            significantFigures += 1

        # sandwiched zero
        elif nonZeroPresent(number[index + 1:]) and passedNonZero:

            # zero is sandwiched thus significant
            significantFigures += 1

    # the number of significant figures in number
    return significantFigures


# returns true if nonzero is present
def nonZeroPresent(numberString):

    # loop through each number/character
    for i in numberString:

        # if i is a non zero
        if i in "123456789":

            # non zero present
            return True

    # no non-zeros in numberString
    return False


print(countSigFigs(input("number here: ")))

