
import re
from MarErrors import InvalidExponentUsage
from MarMath import mono, times


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

    # bad use of exponent
    if "^" in rawEquation and "^{" not in rawEquation:
        raise InvalidExponentUsage

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

    # remember what was last added
    lastWasMonomial = False

    # iterate through spliced data
    for chunkIndex in range(len(splicedMonomials)):

        # iterate through monomials/operators
        for mini in splicedMonomials[chunkIndex]:

            # mini is an operator
            if mini[3] != '':

                # last added was a monomial (and finalEquation has something inside)
                if len(finalEquation) != 0 and isinstance(finalEquation[-1], mono):

                    # add operator to final equation
                    finalEquation.append(mini[3])

                # we just added an operator
                lastWasMonomial = False

            # mini is a number
            elif mini[4] == '':

                # we added a monomial last iteration
                if lastWasMonomial:

                    # multiply the last monomial and the current monomial replace last monomial with result
                    finalEquation[-1] = times(finalEquation[-1], mono(mini[0], {mini[1]: mini[2]}))[0]

                # we didn't just add a monomial
                else:

                    # create a mono and add it to our final equation
                    finalEquation.append(mono(mini[0], {mini[1]: mini[2]}))

                # we just added a monomial
                lastWasMonomial = True

            # mini is a placeholder for a set of brackets
            elif mini[4] != '':

                # add placeholder to finalEquation
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

