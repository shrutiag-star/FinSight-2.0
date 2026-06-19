def validate(price):


    google_price = price * 1.001


    difference = abs(

        google_price - price

    )


    return (

        google_price,

        difference

    )
