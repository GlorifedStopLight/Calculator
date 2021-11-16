import re
from fractions import Fraction


# holds information inside a set of brackets sqrt, abs, (), [], etc
class brackets:
    def __init__(self, equation, bracketType=None):

        # the equation inside of the brackets can be as simple as just one monomial
        self.equation = equation

        # this is None when it's just normal brackets. Otherwise it's a function sqrt, abs, etc
        self.bracketType = bracketType


# monomial class
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
            if self.coefficient != 1:

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


# x monomial minus y monomial
def minus(x, y):

    # the variables and exponents are the same
    if x.variables == y.variables:

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


# divide x monomial by y monomial (x over y)
def dividedBy(x, y):

    # divide both x.co, y.co by this number to get the new x, and y coefficients
    divideBothBy = findGreatestCommonMultiple([x.coefficient, y.coefficient])

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

    # return altered monomials
    return [changedX, '/.', changedY]


# factors a polynomial given 3 monomials
def factorPolynomial(x, y, z):

    # if this is a cubed function
    outside = findCommon([x, y, z])

    # divide each value by their common monomial (outside)
    x = dividedBy(x, outside)
    y = dividedBy(y, outside)
    z = dividedBy(z, outside)



    # find the numbers that will replace y
    yReplacement = findAddToMultiplyTo(y.coefficient, x.coefficient * z.coefficient)

    # make yReplacement into two monomials
    xMiddle = mono(yReplacement[0], y.variables)
    zMiddle = mono(yReplacement[1], y.variables)

    # the value that will be divided out of x and xMiddle
    takeOutOfX = findCommon([x, xMiddle])

    # makes the takeOutOf negative if both are negative
    if x.coefficient < 0 and xMiddle.coefficient < 0:
        takeOutOfX.coefficient = takeOutOfX.coefficient * -1

    # same as takeOutOfX
    takeOutOfZ = findCommon([z, zMiddle])

    # makes the takeOutOf negative if both are negative
    if z.coefficient < 0 and zMiddle.coefficient < 0:
        takeOutOfZ.coefficient = takeOutOfZ.coefficient * -1

    # factor out common factors for x
    x = dividedBy(x, takeOutOfX)
    xMiddle = dividedBy(xMiddle, takeOutOfX)

    # give back the value factored out at the beginning and other stuff
    return outside, takeOutOfX, takeOutOfZ, x, xMiddle


# takes in a list of integers
# returns a common multiple of all of these (integer form)
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
            return commonDivider

    # if at the end of the for loop no common multiple is found then the only common multiple is 1
    return 1


# takes in an array of monomials returns a common monomial
def findCommon(monomials):

    # start big narrow down
    # the first monomial will set the scene

    # all the coefficients from the list of monomials
    allCoefficients = []

    # put all the coefficients into a list
    for co in monomials:
        allCoefficients.append(co.coefficient)

    # find the common multiple of the coefficients
    commonCoefficient = findGreatestCommonMultiple(allCoefficients)

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


# returns human readable string
# takes in an array of values from my factorPolynomial function
def humanReadablePolynomial(poly):

    # value that will be returned
    returnString = ""

    if poly[0].humanReadable() != "1":
        returnString += poly[0].humanReadable()

    returnString += "(" + poly[1].humanReadable() + " + " + poly[2].humanReadable() + ")"
    returnString += "(" + poly[3].humanReadable() + " + " + poly[4].humanReadable() + ")"

    # return string
    return returnString


# solve for solveForMe
def algebra(leftSide, rightSide, solveForMe):
    pass


# takes in 2 monomials and an operator
# if x <op> y is in simplest terms return True else: return False
def isSingleSimplified(x, op, y):

    # adding or subtracting
    if op == "+" or op == "-":

        # can add or subtract
        if x.variables == y.variables:

            # x <op> y is not in simplest terms
            return False

        # can't add or subtract the because variables are not the same
        else:

            # fully simplified
            return True

    # checking if x / y is
    elif op == "/":

        # the coefficients are in lowest terms
        if findGreatestCommonMultiple([x.coefficient, y.coefficient]) == 1:

            # look to see if mono x and mono y have a common variable
            for var in x.variables:

                # var is a shared variable
                if var in y.variables:

                    # not yet simplified
                    return False

            # if the code has reached this point x / y is in simplest terms
            return True

        # at least the coefficients can be simplified further
        else:

            # not fully simplified
            return False


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


# take in an array of monomials and operators in string form (also might have brackets in string form)
def humanReadableEquation(equation):

    # this variable will be returned
    readableEquation = ""

    # loop through all operators and monomials in equation
    for item in equation:

        # item is not a monomial
        if type(item) == str:

            # item is a operator or equal sign
            if item in "+-*/^=":

                # add item to readableEquation with buffer space
                readableEquation += " " + item + " "

            # item is a simplified division
            elif item == "/.":

                # add division to equation
                readableEquation += " / "

            # PROBABLY the only other character it would be is a type of brackets
            else:

                # add brackets (which is item in this instance) to final string
                readableEquation += item

        # found brackets
        elif type(item) == list:

            # turn into string
            bracketHumanReadable = humanReadableEquation(item)

            # add string into readableEquation
            readableEquation += "(" + bracketHumanReadable + ")"

        # must be a monomial (class mono)
        else:
            # readable monomial in string form
            itemReadable = item.humanReadable()

            # negative number
            if '-' in itemReadable:

                # remove negative
                itemReadable = itemReadable.replace("-", "")

                # keeps breaking program idk why
                try:
                    # if something happens and fucks everything up
                    if readableEquation[-2] != "+":

                        print("SOMETHING BAD HAPPENDS")
                        print(readableEquation)
                        # stop program
                        exit()

                except:
                    pass

                # change + negative to subtraction
                readableEquation = readableEquation[:-2] + "- "

            # add a string that represents item to our final string
            readableEquation += itemReadable

    # return a readable representation of given input (equation)
    return readableEquation


# takes an equation (list) with monomials and operators in the form of strings
# returns a simplified equation (list)
def simplifyEquation(equation):

    # check if deepest brackets are simplified
    # if not then check if can distribute into brackets

    # only have 3 elements something like 4 + 2
    # send this to is single simple etc
    smallExpression = []

    # loop for the length of equation - 2
    for index in range(0, len(equation) - 2, 1):

        # index is a nested list (brackets)
        if type(equation[index]) == list:

            # add the nested list to a mini expression
            smallExpression.append(equation[index])

        # smallExpression is a complete expression and is ready to be tested
        if len(smallExpression) == 3:

            # smallExpression not in simplest form
            if not isSingleSimplified(*smallExpression):
                smallExpressionSolved = singleSimplify(smallExpression)


# takes an equation returns an equation with all subtraction replaced with addition and numbers
# that were to the right of the subtraction sign will be multiplied by -1
def purgeSubtraction(equation):

    # remember the current index of the loop
    index = 0

    # loop through the equation
    for item in equation:

        # found subtraction and item is a monomial
        if item == "-" and isinstance(item, mono):

            # change from negative to positive
            equation[index] = "+"

            # modify the number to the right
            equation[index + 1] *= -1

    # this might be redundant because it's a list but whatever
    # return modified equation
    return equation


# finds operators that can not be used because they are already in simplest form
def equationNoBracketsIsFullySimplified(equation):

    # equation is a list with mono type and strings with operators inside
    # the equation does not have brackets
    # equation should go monomial operator monomial operator etc
    # ending and starting with monomial

    # loop through list starting with second element
    # the second element should be an operator
    for index in range(1, len(equation)-1, 1):

        # current index is a operator
        if equation[index] in "*/-+":

            # is not simplified
            if not isSingleSimplified(equation[index-1], equation[index], equation[index+1]):

                # equation is not fully simplified
                return False

    # looped through everything and there is nothing that hasn't been fully simplified
    # equation is fully simplified
    return True


# multiplies equations against each other like foil but with any number of equations with varying length\
# give a list of equations (list of lists)
# these equations should have only addition in them
def megaFoil(allEquations):

    # multiply this bracket with other brackets this bracket changes
    finalEquation = allEquations[0]
    
    print("for loop depth 0")
    # loop through the equations except the very first one
    for equationIndex in range(1, len(allEquations) - 1):

        # each monomial in the finalEquation
        for monomialIndex in range(len(finalEquation)):

            # we have an operator
            if finalEquation[monomialIndex] == "+":

                # go to next iteration of loop
                continue

            # each monomial in the other equation
            for otherMonomial in allEquations[equationIndex]:

                # we have an operator
                if otherMonomial == "+":

                    # go to next iteration of loop
                    continue

                # calculate monomial times monomial
                print("number: ", times(finalEquation[monomialIndex], otherMonomial).humanReadable())
                finalEquation[monomialIndex] = times(finalEquation[monomialIndex], otherMonomial)

    # return the result
    return finalEquation


# takes in an equation in string form, returns a spliced equation
def spliceSingleEquation(rawEquation):

    # 0 or 1 real numbers
    num = "(-?[0-9]*\.?[0-9]*)"

    # any letter 0 or 1 times
    let = "([a-z][A-Z]?)"

    # an exponent
    exponent = "(?:\^{(.*?)})*"

    # full splicer
    full = num + "(?:" + let + exponent + ")?|(/|\*|\+)?" + "|(\[[0-9]*\])"

    # remove all spaces
    noSpaces = rawEquation.replace(" ", "")

    # switch from x - y to x + -y
    monomials = noSpaces.replace("-", "+-")

    # initialize a list
    splicedMonomials = []

    # find number or/and variable or/and exponent
    splicedMonomials.append(re.findall(full, monomials))

    # loop through all numbers
    for nested in splicedMonomials:

        # check for empty list
        while ('', '', '', '', '') in nested:

            # remove empty lists ('', '', '', '', '')
            nested.remove(('', '', '', '', ''))

    # empty list in splicedMonomials
    while [] in splicedMonomials:

        # remove empty list
        splicedMonomials.remove([])

    # initialize the equation return list
    finalEquation = []

    # iterate through spliced data
    for chunkIndex in range(len(splicedMonomials)):

        # iterate through monomials/operators
        for mini in splicedMonomials[chunkIndex]:

            # mini is an operator
            if mini[3] != '':

                # add operator to final equation
                finalEquation.append(mini[3])

            # mini is a number
            elif mini[4] == '':

                # create a mono and add it to our final equation
                finalEquation.append(mono(mini[0], {mini[1]: mini[2]}))

            # mini is a placeholder for a set of brackets
            elif mini[4] != '':
                finalEquation.append(mini[4])

    # give spliced equation
    return finalEquation


# same as spliceSingleEquation but handles parentheses
def spliceFullEquation(rawEquation):

    # re code to get a bracket set
    smallestBracketCode = "\([^(]*?\)"

    # keep track of what should be inserted where (key = location, value = bracket contents)
    bracketDict = {}

    # determines what set of brackets goes where
    bracketsSavedCounter = 0

    # iterate through strings inside equationList
    while "(" in rawEquation:

        # get the set of brackets inside
        bracketInfo = re.search(smallestBracketCode, rawEquation)

        # the location of the bracket set from [bracketIndexes[0] : bracketIndexes[1]]
        bracketIndexes = bracketInfo.span()

        # the content of the brackets
        bracketContent = bracketInfo.group()

        # add bracketContent to our bracketDict
        bracketDict[str(bracketsSavedCounter)] = spliceSingleEquation(bracketContent)

        # replace the contents of the bracket in the string with square brackets and the number that is used to find
        # the corresponding bracket content (from bracketDict)
        rawEquation = rawEquation[:bracketIndexes[0]] + "[" + str(bracketsSavedCounter) + "]" + \
            rawEquation[bracketIndexes[1]:]

        # next iteration of bracket saving
        bracketsSavedCounter += 1

    # splice the changed string
    finalEquationList = spliceSingleEquation(rawEquation)

    # splice string and fill in the bracket placeholders with the corresponding bracket sets
    recursiveSpliceInsert(finalEquationList, bracketDict)

    # finalEquationList is the final output
    return finalEquationList


# a recursive function that takes in a list and returns None
def recursiveSpliceInsert(equationList: list, bracketLocationDict: dict) -> None:

    # equationList is a result of spliceSingleEquation()

    # check for bracket placeholders inside equationList
    for itemIndex in range(len(equationList)):

        # found a string (could be either an operator or a bracket placeholder)
        if type(equationList[itemIndex]) == str:

            # string matches placeholder syntax
            if re.search("\[[0-9]+\]", equationList[itemIndex]):

                # string to pass to bracketLocationDict
                bracketToInsertPlacementNumber = re.findall("\[([0-9]+)\]", equationList[itemIndex])[0]

                # replace placeholder with bracketContents
                equationList[itemIndex] = bracketLocationDict[bracketToInsertPlacementNumber]

                # call this function on the newly added brackets
                recursiveSpliceInsert(equationList[itemIndex], bracketLocationDict)

    # returns nothing changes the equationList list reference
    return None


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


rawEquationInput = "3 * (10 + (4 * 2) + 3) + (6 * 3)"
rawEquationInput = "3 - 2 - 6"  # doesn't work throws an index error
# rawEquationInput = "4 + ((8 - 3) - 4)"


spliced = spliceFullEquation(rawEquationInput)

print("spliced: ", spliced)

readable = humanReadableEquation(spliced)
print("readable: ", readable)

nonReadableAnswer = simplifyNoBracketEquation(spliced)
print(nonReadableAnswer)
print(humanReadableEquation(nonReadableAnswer))





