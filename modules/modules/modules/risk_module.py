import random


def risk_analysis(price):


    volatility = random.uniform(

        8,

        35

    )


    if volatility < 15:

        risk = "LOW"


    elif volatility < 25:

        risk = "MEDIUM"


    else:

        risk = "HIGH"



    return (

        round(

            volatility,

            2

        ),

        risk

    )
