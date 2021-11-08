from random import *

barrel = [False, False, False, False, False, True]

input("press enter to shoot slef 1/6")

dedAmount = 6

while True:

    # ded
    if choice(barrel):
        print("u ded girl")
        break
    else:
        print("not ded yay woooh!")

    dedAmount += 6
    input("press enter to shoot slef 1 / " + str(dedAmount))


