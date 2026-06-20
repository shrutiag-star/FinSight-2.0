import random


def get_data(symbol):


    try:


        import yfinance as yf



        stock=yf.Ticker(

            symbol+".NS"

        )



        hist=stock.history(

            period='5d'

        )



        price=hist['Close'].iloc[-1]



        return {


'price':round(price,2),



'beta':1.0,



'eps':15



}



    except:



        return {


'price':random.randint(


500,


3000


),



'beta':random.uniform(


0.8,


1.5


),



'eps':random.uniform(


10,


40


)



}
