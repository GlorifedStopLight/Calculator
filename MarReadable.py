

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

            # item is simplified addition
            elif item == "+.":

                # add addition to equation
                readableEquation += " + "

            # PROBABLY the only other character it would be is a type of brackets
            else:

                # add brackets (which is item in this instance) to final string
                readableEquation += item

        # found brackets
        elif type(item) == list:

            # turn into string
            bracketHumanReadable = humanReadableEquation(item)

            try:
                # multiplication before brackets
                if readableEquation[-2] == "*":
                    readableEquation = readableEquation[:-3]
            except:
                pass

            # add string into readableEquation
            readableEquation += "(" + bracketHumanReadable + ")"

        # must be a monomial (class mono)
        else:

            # readable monomial in string form
            itemReadable = item.humanReadable()

            # negative number
            if '-' in itemReadable:

                # readableEquation isn't empty and there is an addition operator on the far right
                if len(readableEquation) != 0 and readableEquation[-2] == "+":

                    # remove negative from the monomial
                    itemReadable = itemReadable.replace("-", "")

                    # change + negative to subtraction
                    readableEquation = readableEquation[:-2] + "- "

            # add a string that represents item to our final string
            readableEquation += itemReadable

    # return a readable representation of given input (equation)
    return readableEquation


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
