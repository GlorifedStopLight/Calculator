
PRICES = [7, 1, 5, 3, 6, 4]


#

# returns the greatest profit you can make
def findGreatestProfit(prices):

    # set a baseline for our best profit
    bestProfit = 0

    # baseline
    bestCurrentSellPrice = 0

    # loop through the boobPrices
    for buyPrice in prices:

        # loop through everything after buy price
        for sellPrice in prices[prices.index(buyPrice):]:

            # set bestCurrentSellPrice to something
            bestCurrentSellPrice = sellPrice

            # found a better sell price
            if sellPrice > bestCurrentSellPrice:

                # update best current sell price
                bestCurrentSellPrice = sellPrice

        # we can make something of a profit
        if bestCurrentSellPrice - buyPrice > 0:

            # add this to our possible profit
            bestProfit += bestCurrentSellPrice - buyPrice

    # return the best possible profit
    return bestProfit


print(findGreatestProfit(PRICES))