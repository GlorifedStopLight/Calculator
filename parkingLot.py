# 10-16-2021
import re


def codeMessage(codeThis):
    codeThis = codeThis.split(" ")
    codeThis.reverse()

    twoNested = [codeThis[0::2], codeThis[1::2]]

    for listt in twoNested:

        for wordIndex in range(len(listt)):

            # new word for later
            finishedWord = ""

            for character in listt[wordIndex]:

                finishedWord += str(characterIndex(character)) + " "

            # change word to some numbers
            listt[wordIndex] = finishedWord[::-1]

    return twoNested


def characterIndex(char):
    global Pandemic

    for i in range(len(alphaBet)):
        if alphaBet[i] == char:
            return i


def decode(bigList):
    global Pandemic

    # go through the two nested lists
    for nested in bigList:

        # loop through each "word"
        for wordIndex in range(len(nested)):

            # reverse string
            nested[wordIndex] = nested[wordIndex][::-1]

            # decoded word
            finishedWord = ""

            # loop through the letters in word
            for char in nested[wordIndex].split(" "):
                try:
                    finishedWord += alphaBet[int(char)]
                except ValueError:
                    continue

            nested[wordIndex] = finishedWord

    newList = []

    for list1, list2 in zip(bigList[0], bigList[1]):
        newList.append(list1)
        newList.append(list2)

    newList.reverse()
    string = ""
    for i in newList:
        string += i + " "
    return string


alphaBet = "abcdefghijk:ABCDEFGHIJKL/MNOPlmno*pqrstu.vwxyz ',I#1234567890"

message = "me: #55CDFC #F7A8B8 #FFFFFF #F7A8B8 #55CDFC"
# 55CDFC #F7A8B8 #FFFFFF #F7A8B8 #55CDFC"

print(message)
print(codeMessage(message))