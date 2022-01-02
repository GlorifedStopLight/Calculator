from MarSplicer import spliceFullEquation
from MarMath import *
from math import inf


# answers the problems that the user gives it
def slaveToUser(funMath, listOfInputs):

    # splice the user's input
    listOfSplicedInput = [spliceFullEquation(listOfInputs[i]) for i in range(len(listOfInputs))]

    # answer question
    answerToQuestion = funMath(*listOfSplicedInput)

    # change it so that the answer is readable
    answerToQuestion = humanReadableEquation(answerToQuestion)

    # show answer
    print(answerToQuestion)


# [0] = function name   [1] = test input   [2] = number of arguments (inf = any number)
options = [
    [polyLongDivision, ["3x^{4} - 4x^{2} + 1", "x + 1"], 2],
    [findAddToMultiplyTo, [[-3, 9]], 1],
    [findGreatestCommonMultiple, [9, 27, 12], inf]
]


slaveToUser(options[0][0], options[0][1])
