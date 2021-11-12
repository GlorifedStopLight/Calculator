

testList = [4, "+", 5, "+", 10]

newForLoop = True
while newForLoop == True:

    newForLoop = False
    # loop through test list
    for i in range(len(testList)):

        if testList[i] == "+":
            # i + 1
            num2 = testList.pop(i+1)

            num1 = testList.pop(i-1)

            testList.insert(i-1, num1+num2)

            del testList[i]

            newForLoop = True

            break

print(testList)

