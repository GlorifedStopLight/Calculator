from MarMath import polyLongDivision, humanReadableEquation
from MarSplicer import spliceFullEquation

rawEquation1 = "3x^{4} - 4x^{2} + 1"

rawEquation2 = "x + 1"

print(humanReadableEquation(spliceFullEquation(rawEquation1)))
print("/")
print(humanReadableEquation(spliceFullEquation(rawEquation2)))

newPoly = polyLongDivision(spliceFullEquation(rawEquation1), spliceFullEquation(rawEquation2))

print()
print(humanReadableEquation(newPoly))

#print(findAddToMultiplyTo(1, 5*-18))
#print(findGreatestCommonMultiple([35, 49]))