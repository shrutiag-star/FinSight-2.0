def portfolio_summary(results):

    high = 0
    medium = 0
    low = 0


    for stock in results:

        if stock['Risk'] == "HIGH":

            high += 1


        elif stock['Risk'] == "MEDIUM":

            medium += 1


        else:

            low += 1


    return high, medium, low
