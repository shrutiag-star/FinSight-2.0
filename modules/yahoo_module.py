import yfinance as yf


def get_data(symbol):

    stock = yf.Ticker(symbol + ".NS")

    info = stock.info


    return {

        'price': info.get('currentPrice', 0),

        'marketcap': info.get('marketCap', 0),

        'beta': info.get('beta', 0),

        'eps': info.get('trailingEps', 0),

        'volume': info.get('volume', 0)

    }
