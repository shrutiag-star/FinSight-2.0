from tradingview_ta import TA_Handler


def technical(symbol):

    stock = TA_Handler(

        symbol=symbol,

        screener="india",

        exchange="NSE",

        interval="1d"

    )


    analysis = stock.get_analysis()


    return {

        'RSI': analysis.indicators['RSI'],

        'MACD': analysis.indicators['MACD.macd'],

        'Recommendation': analysis.summary['RECOMMENDATION']

    }
