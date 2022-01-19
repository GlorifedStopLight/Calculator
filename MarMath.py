from fractions import Fraction


# monomial class
from MarReadable import humanReadableEquation


class mono:
    def __init__(self, coefficient, variables):

        # no coefficient
        if coefficient == '':

            # set coefficient to default
            self.coefficient = Fraction(1).limit_denominator()

        # coefficient given
        else:
            # set coefficient to a fraction type
            self.coefficient = Fraction(float(coefficient)).limit_denominator()

        # iterate through variables
        for var in variables.copy():

            # no variable given
            if var == '':
                del variables[var]

            # no exponent given
            elif variables[var] == '':

                # set var's exponent to the default of 1
                variables[var] = Fraction(1).limit_denominator()

            # var has an exponent that isn't 1
            else:

                # change from a string to a fraction
                variables[var] = Fraction(variables[var]).limit_denominator()

        # this would be a dictionary of letters and their corresponding exponents like so:
        # {'x': 3, 'y': 1}, by default this dictionary is empty
        self.variables = variables

    # called on after any operation (pemdas)
    def pemdasCleanUp(self):

        # coefficient is 0 (bad, fix this here)
        if self.coefficient == 0:

            # 0 times any variable is 0, set variables to None (exponents also are removed)
            self.variables = {}

        # check all the variables to make sure no zero exponents
        for var in self.variables.copy():

            # there is a variable that has a zero exponent
            if self.variables[var] == 0:

                # remove this variable
                self.variables.pop(var)

        # return this instance of mono
        return self

    # returns a human readable string
    def humanReadable(self):

        # the return variable
        returnString = ""

        # no variables
        if self.variables == {}:

            # co is the same value even if it was an integer
            if self.coefficient == int(self.coefficient):

                # return just the coefficient (remove decimal point with int() )
                return str(int(self.coefficient))

            # co is a float that will not be the same if converted to an integer
            else:

                # return the coefficient as a string
                return str(self.coefficient)

        # variables present
        else:

            # show coefficient
            if abs(self.coefficient) != 1:

                # co is the same value even if it was an integer
                if self.coefficient == int(self.coefficient):

                    # save just the coefficient (remove decimal point with int() )
                    returnString += str(int(self.coefficient))

                # co is a float with non zeros after the decimal point
                else:

                    # save the coefficient as a string
                    returnString += "(" + str(self.coefficient) + ")"

            # add all the variables and exponents to the return string
            for var in self.variables:

                # has a negative coefficient
                if self.coefficient < 0:

                    # add a negative sign
                    returnString += "-"

                # add the letter to the string
                returnString += var

                # if the exponent is 1 it shouldn't be shown
                if self.variables[var] > 1:

                    # add to return string
                    returnString += "^{" + str(self.variables[var]) + "}"

        # return string
        return returnString

    # plugs in variables for this monomial and returns the result
    def plugInVariables(self, variableValues):

        # variableValues is a dictionary of variable names and their values accordingly
        # ex:  {"x": 10}  x = 10

        # assume that every variable in variableValues is a variable in this monomial

        # loop through each variable in dictionary
        for var in variableValues:

            # coefficient times (the plug in number) to the power of the exponent of var
            # ex: x=4,  3x^3 --> ( [new]coefficient = 3(4)^3 )
            self.coefficient *= variableValues[var] ** self.variables[var]

            # remove the variable & exponent from the this monomial
            del self.variables[var]

        return mono(self.coefficient, self.variables).pemdasCleanUp()


# simplifies a equation with no brackets
def simplifyNoBracketEquation(equation):

    # determines whether or not to start a new for loop
    newForLoop = True

    # when we want another for loop
    while newForLoop:

        # if we don't find any operators in the equation we will stop
        newForLoop = False

        # set index for the while loop
        customIndex = 0

        # set the length of the equation
        lengthOfEquation = len(equation)

        # iterate through equation with custom for loop
        while customIndex < lengthOfEquation:

            # on a monomial not an operator
            # current is subtraction/addition but there is multiplication/division (NEXT ITERATION)
            if type(equation[customIndex]) != str or \
                    "*" in equation and equation[customIndex] in "+-" or \
                    "/" in equation and equation[customIndex] in "+-":

                # go to next iteration
                customIndex += 1
                continue

            # either multiplication or division
            if equation[customIndex] in "*/":

                # do multiplication
                if equation[customIndex] == "*":

                    # solve part of the equation
                    miniAnswer = times(equation.pop(customIndex-1), equation.pop(customIndex))

                    # remove operator
                    del equation[customIndex - 1]

                    # loop through elements
                    for itemIndex in range(len(miniAnswer)):

                        # add miniAnswer to equation
                        equation.insert(customIndex + itemIndex - 1, miniAnswer[itemIndex])

                    # make a new for loop
                    newForLoop = True

                    # end this one
                    break

                # do division
                if equation[customIndex] == "/":

                    # solve part of the equation
                    miniAnswer = dividedBy(equation.pop(customIndex-1), equation.pop(customIndex))

                    # remove operator
                    del equation[customIndex - 1]

                    # loop through elements of mini answer
                    for itemIndex in range(len(miniAnswer)):

                        # add miniAnswer to equation
                        equation.insert(customIndex + itemIndex - 1, miniAnswer[itemIndex])

                    # make a new for loop
                    newForLoop = True

                    # end this one
                    break

            # there is either addition or subtraction
            elif equation[customIndex] in "+-":

                # do addition
                if equation[customIndex] == "+":

                    # solve part of the equation
                    miniAnswer = plus(equation.pop(customIndex-1), equation.pop(customIndex))

                    # remove operator
                    del equation[customIndex - 1]

                    # loop through elements of mini answer
                    for itemIndex in range(len(miniAnswer)):

                        # add miniAnswer to equation
                        equation.insert(customIndex + itemIndex - 1, miniAnswer[itemIndex])

                    # there was nothing inside miniAnswer
                    if miniAnswer == []:

                        # something already in equation
                        if equation:

                            # remove unused operator
                            del equation[customIndex-1]

                    # make a new for loop
                    newForLoop = True

                    # end this one
                    break

                # do subtraction
                else:

                    # panic
                    print("there is subtraction PANIC")
                    exit()

            # next iteration of custom for loop
            customIndex += 1

            # reset the length of the equation variable
            lengthOfEquation = len(equation)

    # return simplified equation
    return equation


# x monomial minus y monomial
def minus(x, y):

    # the variables and exponents are the same
    if x.variables == y.variables:

        # no point in returning zero
        if x.coefficient - y.coefficient == 0:

            # give back an empty list
            return []

        # return answer
        return [mono(x.coefficient - y.coefficient, x.variables).pemdasCleanUp()]

    # variables or exponents are NOT the same
    else:

        # return the monomials unchanged with operator
        # period shows it's in simplest form
        return [x, '-.', y]


# x monomial plus y monomial
def plus(x, y):

    # the variables and exponents are the same
    if x.variables == y.variables:

        # no point in returning zero
        if x.coefficient + y.coefficient == 0:

            # give an empty list
            return []

        # return answer
        return [mono(x.coefficient + y.coefficient, x.variables).pemdasCleanUp()]

    # variables or exponents are NOT the same
    else:

        # return the monomials unchanged with operator
        # period shows that this is in simplest form
        return [x, '+.', y]


# x monomial times y monomial
def times(x, y):

    # calculate the coefficient
    newCoefficient = x.coefficient * y.coefficient

    # merge the two dictionaries
    newVariables = multiplyMonoVariables(x.variables, y.variables)

    # create new mono object and return
    return [mono(newCoefficient, newVariables).pemdasCleanUp()]


# divide x monomial by y monomial (x over y)
def dividedBy(x, y):

    # divide both x.co, y.co by this number to get the new x, and y coefficients
    divideBothBy = findCommonMono([x, y]).coefficient

    # calculate new coefficients from 4/8 ---> 1/2
    changedXCoefficient = x.coefficient / divideBothBy
    changedYCoefficient = y.coefficient / divideBothBy

    newCoefficient = Fraction(x.coefficient / y.coefficient)

    # merge the two dictionaries
    twoChangedVariables = divideMonoVariables(x.variables, y.variables)

    # the new numerator (x)
    changedX = mono(changedXCoefficient, twoChangedVariables[0]).pemdasCleanUp()

    # new denominator (y)
    changedY = mono(changedYCoefficient, twoChangedVariables[1]).pemdasCleanUp()

    # changedX is over 1 just return changedX
    if len(changedY.variables) == 0 and changedY.coefficient == 1:

        # return just changedX
        return [changedX]

    # return altered monomials
    return [changedX, '/.', changedY]


# takes in 2 dictionaries that represent variables from monomials
def divideMonoVariables(variables1, variables2):

    # create copies of both dictionaries to keep the originals the same
    variables1 = variables1.copy()
    variables2 = variables2.copy()

    # go through each variable in variables1
    for var in variables1:

        # var is a common variable (both dictionaries have it in common)
        if var in variables2:
            # subtract exponents
            variables1[var] -= variables2[var]

            # variable has been canceled out, remove from dictionary
            del variables2[var]

    # return divided variables
    return variables1, variables2


# takes in two dictionaries returns a dictionary with all keys
# if dictionaries have a common key add the values of that key from each dictionary
def multiplyMonoVariables(dict1, dict2):

    # copy of dict1
    newDict = dict1.copy()

    # newDict now has the keys from both dict1 and dict2
    newDict.update(dict2)

    # loop through all the common keys (newDict's keys)
    for key in newDict:

        # key is common among both dict1 and dict1
        if key in dict1 and key in dict2:

            # add exponents from common variables
            newDict[key] = dict1[key] + dict2[key]

        # key is unique to dict1
        elif key in dict1:

            # key = value1
            newDict[key] = dict1[key]

        # key must be only in dict2
        else:

            # key = value2
            newDict[key] = dict2[key]

    # return the merged dictionary
    return newDict


# do sqrt on a monomial
def XRootOfSingleY(x: int, y: mono):

    # the end result of simplification
    endResult = []

    # y has a negative coefficient and an even root (bad -> simplification will return a imaginary number)
    if x % 2 == 0 and y.coefficient <= 0:

        # return given monomial (no change)
        return [y]

    # coefficient can be simplified
    if (y.coefficient ** round((1/x))**x) == y.coefficient:
        endResult.append(None)


# takes an equation (list) with monomials and operators in the form of strings
# returns a simplified equation (list)
def simplifyFullEquation(equation):

    # check if deepest brackets are simplified
    # if not then check if can distribute into brackets

    # only have 3 elements something like 4 + 2
    # send this to is single simple etc

    # iterate through equation
    for item in equation:

        # item is a set of brackets
        if type(item) == list:

            pass


def factorPolynomial(poly):

    # TODO: factor by difference of squares, factor by grouping, factor out

    # get all monomials inside poly
    monomialsInsidePoly = findMonomialsInEquation(poly)

    # find the commonFactor of the monomials
    commonFactor = findCommonMono(monomialsInsidePoly)

    # common factor isn't just 1
    if commonFactor != 1:

        # iterate through each item in the polynomial
        for itemIndex in range(len(poly)):

            # item is a monomial
            if isinstance(poly[itemIndex], mono):

                # divide everything in the polynomial by our commonFactor
                poly[itemIndex] = dividedBy(poly[itemIndex], commonFactor)[0]

        # add common factor outside of polynomial
        poly = [commonFactor, "*", poly]

    # return factored out polynomial
    return poly


# takes in a list of monomials and groups them in brackets accordingly must be an even number of monomials
def factorPolynomialByGrouping(poly):

    # ask Renae about what makes a polynomial eligible for grouping
    pass


# assume the given polynomial is able to be factored using difference of squares return result
def factorPolynomialByDifferenceOfSquares(poly):
    pass


# sorts a polynomial from the greatest exponent on the left to the lowest exponent on the right
def sortPolynomialProper(poly):

    # the sorted polynomial
    sortedPoly = findMonomialsInEquation(poly)

    # sort the list
    sortedPoly.sort(key=findExponentValues)

    # reverse the list
    sortedPoly.reverse()

    # loop through equation add an addition operator in between each monomial
    for index in range(1, len(sortedPoly)*2 - 1, 2):

        # insert + in list
        sortedPoly.insert(index, "+")

    # return a sorted polynomial
    return sortedPoly


# subtracts one polynomial (x) from the other (y)
def polyMinusPoly(x, y):

    # distribute the negative
    negativeY = polyTimesPoly(y, [mono(-1, {})])

    # add two polynomials together and return that value
    return polyPlusPoly(x, negativeY)


# takes two polynomials (a list of monomials with addition operators) returns result
def polyTimesPoly(x, y):

    # new polynomial
    unsimplifiedNewPolynomial = []

    # iterate through each monomial in x
    for itemX in x:

        # itemX is a monomial not an operator
        if isinstance(itemX, mono):

            # iterate through each monomial in y
            for itemY in y:

                # itemY is also a monomial
                if isinstance(itemY, mono):

                    # multiply both monomials together
                    resultOfItems = times(itemX, itemY)

                    # add the itemX * itemY to our unsimplified polynomial
                    unsimplifiedNewPolynomial.append(resultOfItems[0])

                    # add an operator
                    unsimplifiedNewPolynomial.append("+")

    # remove the last element of the list (this is going to be an addition operator)
    unsimplifiedNewPolynomial.pop(-1)

    simplifyNoBracketEquation(unsimplifiedNewPolynomial)

    # return new polynomial
    return unsimplifiedNewPolynomial


# adds two polynomials together
def polyPlusPoly(x, y):

    # take out all the monomials in both lists and put them into the same list
    simplifyMe = [*x, "+", *y]

    # sort the polynomial
    simplifyMe = sortPolynomialProper(simplifyMe)

    # return the polynomial simplified
    return simplifyNoBracketEquation(simplifyMe)


# takes two polynomials divides them returns stuff etc
def polyLongDivision(dividend, divisor):

    # the result of dividend / divisor
    endResult = []

    # the term at the front of divisor
    divisorFrontTerm = divisor[0]

    # the variable name
    variableName = list(dividend[0].variables.keys())[0]

    # stop when the front number in the dividend has an exponent less than that of the divisor's front end exponent
    while dividend and dividend[0].variables != {} and dividend[0].variables[variableName] >= divisor[0].variables[variableName]:

        # the term at the front of dividend
        dividendFrontTerm = dividend[0]

        # the number that when multiplied by the divisor front term will equal the dividend front term
        singleUpperTable = dividedBy(dividendFrontTerm, divisorFrontTerm)

        # add this to our end result
        for i in singleUpperTable:

            endResult.append(i)
        endResult.append("+")

        # the polynomial that will be subtracted from the dividend
        subtractThisPolynomial = polyTimesPoly(singleUpperTable, divisor)

        # subtract (subtractThisPoly) from dividend
        dividend = polyMinusPoly(dividend, subtractThisPolynomial)

    # no remainder
    if not dividend:

        # remove the addition sign at the end of equation
        endResult.pop(-1)

    # add the remainder to the endResult
    else:

        # add remainder to result
        endResult.append([dividend, "/", divisor])

    # return the result of divisor/dividend
    return endResult


# input an equation returns true if equation can be factored using difference of squares otherwise -> false
def polyCanUseDifferenceOfSquares(poly):

    # holds the monomials in polynomial
    monomials = []

    # loop through the polynomial
    for item in poly:

        # item is monomial
        if isinstance(item, mono):

            # add item to monomials list
            monomials.append(item)

    # not exactly two monomials in poly
    if len(monomials) != 2:

        # can not be factored using difference of squares
        return False

    # either both or neither monomials are negative
    if (monomials[0].coefficient < 0) != (monomials[1].coefficient < 0):

        # can not be factored using difference of squares
        return False

    # check if numbers can be used with with square root



    # all conditions have been met poly can be factored using difference of squares
    return True


# multiplies equations against each other like foil but with any number of equations with varying length\
# give a list of equations (list of lists)
# these equations should have only addition in them
def megaFoil(allPolynomials):
    # multiply this bracket with other brackets this bracket changes
    finalEquation = allPolynomials[0]

    print("for loop depth 0")
    # loop through the equations except the very first one
    for equationIndex in range(1, len(allPolynomials) - 1):

        # each monomial in the finalEquation
        for monomialIndex in range(len(finalEquation)):

            # we have an operator
            if finalEquation[monomialIndex] == "+":
                # go to next iteration of loop
                continue

            # each monomial in the other equation
            for otherMonomial in allPolynomials[equationIndex]:

                # we have an operator
                if otherMonomial == "+":
                    # go to next iteration of loop
                    continue

                # calculate monomial times monomial
                print("number: ", times(finalEquation[monomialIndex], otherMonomial).humanReadable())
                finalEquation[monomialIndex] = times(finalEquation[monomialIndex], otherMonomial)

    # return the result
    return finalEquation


def findGreatestCommonMultiple(integers):

    # make sure all the values in this list are positive
    integers = [abs(i) for i in integers]

    # sort the list from lowest to highest
    integers.sort()

    # remember the smallest number
    smallest = integers[0]

    # start at the greatest number possible and work your way down to 1
    for commonDivider in range(int(smallest), 0, -1):

        # true until proven false
        foundGreatestCommonMultiple = True

        # all the integers
        for num in integers:

            # num is not evenly divisible by commonDivider
            if num % commonDivider != 0:

                # we have not found the greatest common multiple
                foundGreatestCommonMultiple = False

                # go to the next iteration where commonDivider is different
                break

        # found the greatest common multiple
        if foundGreatestCommonMultiple:

            # return commonDivider
            return commonDivider

    # if at the end of the for loop no common multiple is found then the only common multiple is 1
    return 1


# takes in an array of monomials returns a common monomial
def findCommonMono(monomials):

    # start big narrow down
    # the first monomial will set the scene

    # all the coefficients from the list of monomials
    allCoefficients = []

    # put all the coefficients into a list
    for co in monomials:
        allCoefficients.append(co.coefficient)

    # find the common multiple of the coefficients
    commonCoefficient = findGreatestCommonMultiple(allCoefficients)

    # all coefficients are negative
    if all([num < 0 for num in allCoefficients]):

        # make commonCoefficient negative
        commonCoefficient *= -1

    # fill this variable with something then slowly remove from it
    commonVariables = monomials[0].variables.copy()

    # loop through all of the monomials
    for m in monomials:

        # loop through the commonVariables
        for var in commonVariables.copy():

            # var is not common
            if var not in m.variables:

                # remove var
                commonVariables.pop(var)

            # check the exponent of var
            else:

                # variable has an exponent that is too big
                if commonVariables[var] > m.variables[var]:

                    # lower the common exponent for 'var'
                    commonVariables[var] = m.variables[var]

    # return a monomial that has something in common with the values given
    return mono(commonCoefficient, commonVariables)


# finds the pair of numbers that adds to (addTo) and multiplies to (multiplyTo)
def findAddToMultiplyTo(addTo, multiplyTo):

    # find values that can be evenly divided from multiplyTo
    for evenDivider in range(abs(int(multiplyTo/2)), 0, -1):

        # can be evenly divided
        if multiplyTo % evenDivider == 0:

            # evenDivider * otherNum = multiplyTo
            otherNum = abs(multiplyTo) // evenDivider

            # otherNum and evenDivider are both positive or both negative
            if multiplyTo > 0:

                # return these numbers if they add to addTo
                if otherNum + evenDivider == addTo:
                    return otherNum, evenDivider

                # return if they add to addTo
                elif (otherNum * -1) + (evenDivider * -1) == addTo:
                    return otherNum * -1, evenDivider * -1

            # multiplyTo is negative
            else:

                # return these numbers if they add to addTo
                if otherNum * -1 + evenDivider == addTo:
                    return otherNum * -1, evenDivider

                # return if they add to addTo
                elif otherNum + evenDivider * -1 == addTo:
                    return otherNum, evenDivider * -1


# takes an equation, returns a list of monomials inside equation (works with brackets)
def findMonomialsInEquation(equation):

    # a list of all monomials inside equation
    allMonomials = []

    # iterate through equation's items
    for item in equation:

        # item is a monomial
        if isinstance(item, mono):

            # add item to our list of monomials
            allMonomials.append(item)

        # item is a set of brackets (a mini equation)
        elif type(item) == list:

            # add each nested monomial inside of brackets (item) to our all monomials list
            for nestedMonomial in findMonomialsInEquation(item):
                allMonomials.append(nestedMonomial)

    # return list of monomials inside equation
    return allMonomials


# takes a monomial returns the value of the first exponent
def findExponentValues(monomial):

    # monomial has a variable
    if len(monomial.variables.keys()) != 0:

        # return the exponent
        return int(list(monomial.variables.values())[0])

    # monomial has no variable
    else:

        # value of the exponent for the variable is 0
        return 0


# expands a single logarithm
def expandSingleLogarithm(equation, logBase):
    pass