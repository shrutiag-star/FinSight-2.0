from modules.forecast_module import *
from modules.sentiment_module import sentiment
from modules.yahoo_module import get_data

import time
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import yfinance as yf
###################################################
# Dynamic Company Information
###################################################

@st.cache_data
def get_company_info(symbol):

    try:

        ticker = yf.Ticker(

            f"{symbol}.NS"

        )

        info = ticker.info


        return {

    'Sector':

    info.get(

        'sector',

        'Unknown'

    ),


    'Industry':

    info.get(

        'industry',

        'Unknown'

    ),


    'Beta':

    info.get(

        'beta',

        1

    ),


    'MarketCap':

    info.get(

        'marketCap',

        0

    ),


    'Country':

    info.get(

        'country',

        'India'

    ),


    'DividendYield':

    info.get(

        'dividendYield',

        0

    ),


    'QuoteType':

    info.get(

        'quoteType',

        'EQUITY'

    )

}


    except:



        return {


            'Sector':'Unknown',

            'Industry':'Unknown',

            'Beta':1,

            'MarketCap':0,

            'Country':'India',

            'DividendYield':0


        }

import plotly.graph_objects as go
from streamlit.components.v1 import html


###################################################
# Page Config
###################################################

st.set_page_config(

    page_title="FinSight 2.0",

    page_icon="📈",

    layout="wide"

)

st.markdown(

"""

<style>


html,


body,


[class*="css"]{


font-family:Arial;


font-size:17px;


}



h1{


font-size:48px;


color:#00C8FF;


}



h2{


font-size:34px;


}



h3{


font-size:28px;


}



[data-testid="metric-container"]{


background:#202632;


padding:15px;


border-radius:10px;


box-shadow:0px 0px 6px black;


}



</style>


""",


unsafe_allow_html=True


)

###################################################
# Top Bar
###################################################

left,right = st.columns([3,1])

with left:

    st.caption(

        f"Last Updated : {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"

    )


with right:

    st.caption(

        "Status : 🟢 Live"

    )


###################################################
# Title
###################################################

st.title(

    "🧠 FinSight 4.0"

)


st.subheader(

    "Investor Portfolio Intelligence Platform"

)



###################################################
# Investor Profile
###################################################

st.sidebar.header(

    "Investor Profile"

)


capital = st.sidebar.number_input(

    "Investment Amount",

    10000,

    10000000,

    100000

)


risk = st.sidebar.selectbox(

    "Risk Appetite",

    [

        "Low",

        "Medium",

        "High"

    ]

)

years = st.sidebar.slider(

    "Investment Horizon",

    1,

    30,

    5

)

###################################################
# SIP Planner
###################################################

st.sidebar.markdown(

"---"

)

st.sidebar.subheader(

"🎯 SIP Planner"

)


sip = st.sidebar.number_input(

"Monthly SIP",

1000,

100000,

10000

)


r = 0.12/12


n = years*12


future = sip*((1+r)**n-1)/r


future = round(

future,

0

)


st.sidebar.metric(

"Expected Corpus",

f"₹{future:,.0f}"

)



###################################################
# Retirement Planner
###################################################

st.sidebar.markdown(

"---"

)

st.sidebar.subheader(

"🏖 Retirement Planner"

)


age = st.sidebar.slider(

"Current Age",

20,

60,

25

)


retire = st.sidebar.slider(

"Retirement Age",

55,

70,

60

)


expense = st.sidebar.number_input(

"Monthly Expense",

10000,

500000,

50000

)


inflation = 0.06


yrs = retire-age


corpus = (

expense*12*25

)*(

1+inflation

)**yrs


corpus = round(

corpus,

0

)


st.sidebar.metric(

"Required Corpus",

f"₹{round(corpus/10000000,2)} Cr"

)


###################################################
# Upload Portfolio
###################################################

uploaded = st.file_uploader(

    "📂 Upload Portfolio Statement",

    type=[

        'csv',
        'xlsx',
        'xls',
        'txt',
        'pdf',
        'docx'

    ]

)


import os


###################################################
# User Upload
###################################################

import os

if uploaded is not None:

    filename = uploaded.name.lower()

    if filename.endswith('.csv'):

        portfolio = pd.read_csv(uploaded)

    elif filename.endswith(('.xlsx', '.xls')):

        portfolio = pd.read_excel(uploaded)

    elif filename.endswith('.txt'):

        portfolio = pd.read_csv(
            uploaded,
            sep='\t'
        )

    elif filename.endswith('.pdf'):

        st.warning("PDF parser will be added later")

        portfolio = pd.DataFrame(
            columns=['Stock', 'Quantity']
        )

    elif filename.endswith('.docx'):

        st.warning("DOCX parser will be added later")

        portfolio = pd.DataFrame(
            columns=['Stock', 'Quantity']
        )

else:

    path = os.path.join(
        os.getcwd(),
        'portfolio.csv'
    )

    portfolio = pd.read_csv(path)


###################################################
# Cleaning
###################################################

portfolio.columns = [
    str(x).strip()
    for x in portfolio.columns
]


rename = {

    'Company': 'Stock',
    'Shares': 'Quantity',
    'Units': 'Quantity',
    'Symbol': 'Stock',
    'Qty': 'Quantity'

}


portfolio.rename(

    columns=rename,

    inplace=True

)


required = {

    'Stock',

    'Quantity'

}


if not required.issubset(portfolio.columns):

    st.error(

        "Portfolio must contain Stock and Quantity columns"

    )

    st.stop()


portfolio['Stock'] = portfolio['Stock'].astype(str)


portfolio['Quantity'] = pd.to_numeric(

    portfolio['Quantity'],

    errors='coerce'

)


portfolio.dropna(

    inplace=True

)


###################################################
# Preview
###################################################

st.subheader(

    "Portfolio Preview"

)

st.dataframe(

    portfolio,

    use_container_width=True

)



###################################################
# Sidebar
###################################################

st.sidebar.title(

    "Controls"

)



selected = st.sidebar.multiselect(

    "Select Stocks",

    portfolio['Stock'],

    default=portfolio['Stock']

)



search = st.sidebar.text_input(

    "Search Stock"

)



if search:


    portfolio = portfolio[


        portfolio['Stock'].str.contains(

            search,

            case=False

        )

    ]



portfolio = portfolio[


    portfolio['Stock'].isin(

        selected

    )

]



if len(portfolio) > 0:

    stock = st.sidebar.selectbox(

        "Analyse Stock",

        portfolio['Stock']

    )

else:

    st.error(

        "No stocks available."

    )

    st.stop()




###################################################
# Analysis
###################################################

analysis_start = time.time()



prices = []

recommendations = []

confidence = []

sentiments = []



for _, row in portfolio.iterrows():

    data = get_data(row['Stock'])

    price = data['price']
    beta = data['beta']

    prices.append(price)

    dummy_news = f"""

    {row['Stock']} announced quarterly results.

    Institutional investors increased holdings.

    Revenue growth remained stable.

    """

    news = sentiment(dummy_news)

    sentiments.append(news)


    if beta < 0.8:

        recommendations.append("BUY")

        confidence.append(80)


    elif beta < 1.3:

        recommendations.append("HOLD")

        confidence.append(65)


    else:

        recommendations.append("SELL")

        confidence.append(40)


analysis_end = time.time()



analysis_time = round(

    analysis_end

    -

    analysis_start,

    2

)



###################################################
# Dynamic Asset Detection
###################################################

asset_class = []

for stock in portfolio['Stock']:

    stock = str(stock).upper().strip()

    # Crypto
    if "-USD" in stock:

        asset_class.append("Crypto")

    # Forex
    elif "=X" in stock:

        asset_class.append("Forex")

    # ETF
    elif "BEES" in stock or "ETF" in stock:

        asset_class.append("ETF")

    # Mutual Fund
    elif "PPFAS" in stock:

        asset_class.append("Mutual Fund")

    # Bond
    elif "BOND" in stock:

        asset_class.append("Bond")

    # Everything else
    else:

        asset_class.append("Equity")


portfolio['Asset Class'] = asset_class



###################################################
# Portfolio Data
###################################################

portfolio['Price'] = prices



portfolio['Value'] = (


    portfolio['Price']

    *

    portfolio['Quantity']


)



portfolio['Recommendation'] = recommendations
st.write(

len(portfolio),

len(prices),

len(recommendations),

len(confidence),

len(sentiments)

)

portfolio['Confidence'] = confidence


portfolio['Sentiment'] = sentiments




###################################################
# Timer
###################################################

st.success(

    f"⏱ Analysis Time : {analysis_time} sec"

)



###################################################
# Portfolio Summary
###################################################

st.header(

"📊 Executive Dashboard"

)



c1,c2,c3,c4,c5,c6 = st.columns(

6

)



c1.metric(

    "Stocks",

    len(portfolio)

)



c2.metric(

    "Portfolio Value",

    round(

        portfolio['Value'].sum(),

        2

    )

)



c3.metric(

    "Average Price",

    round(

        portfolio['Price'].mean(),

        2

    )

)



c4.metric(

    "Total Quantity",

    portfolio['Quantity'].sum()

)



if len(portfolio)>0:


    largest = portfolio.loc[


        portfolio['Value'].idxmax()


    ]


else:


    largest = pd.Series(

        {

            'Stock':'NA',

            'Value':0

        }

    )



c5.metric(

    "Largest Holding",

    largest['Stock']

)

# c6.metric(

# "FinSight Score",

# score

# )




###################################################
# Holdings
###################################################

st.header(

    "Portfolio Holdings"

)

st.metric(

    "Asset Classes Detected",

    portfolio['Asset Class'].nunique()

)



st.dataframe(

    portfolio,

    use_container_width=True

)




###################################################
# Correlation Matrix
###################################################

st.header(

"Correlation Matrix"

)



corr=portfolio[[

'Price',

'Value'

]].corr()



st.dataframe(

corr

)



###################################################
# Portfolio Health
###################################################

health = 0

health += portfolio['Confidence'].mean()*0.5

health += (

100

-

portfolio['Quantity'].std()

)*0.2



health += 20



health = round(

min(

health,

100

),

2

)



st.header(

"Portfolio Health"

)



st.progress(

int(

health

)

)



st.success(

f"Portfolio Health Score : {health}/100"

)



###################################################
# FinSight Score
###################################################

score = (

health*0.6

+

portfolio['Confidence'].mean()*0.4

)

score = round(

score,

2

)



###################################################
# Market Mood
###################################################

avg = portfolio['Confidence'].mean()


if avg > 75:

    mood = "🟢 Bullish"


elif avg > 55:

    mood = "🟡 Neutral"


else:

    mood = "🔴 Bearish"



st.header(

"Market Mood"

)


st.info(

mood

)


###################################################
# Top Performer
###################################################

top = portfolio.loc[


portfolio['Confidence'].idxmax()


]



st.header(

"Top Performer Prediction"

)


st.success(

f"{top['Stock']} has "

f"{top['Confidence']}% confidence "

"to outperform others."

)


###################################################
# Charts
###################################################

col1,col2 = st.columns(2)


with col1:


    st.subheader(

        "Asset Allocation"

    )


    fig1 = px.pie(

        portfolio,

        names='Asset Class',

        values='Value',

        hole=0.4

    )


    fig1.update_layout(

        template='plotly_dark',

        height=500

    )


    st.plotly_chart(

        fig1,

        use_container_width=True

    )



with col2:


    st.subheader(

        "Holdings Comparison"

    )


    fig2 = px.bar(

        portfolio,

        x='Stock',

        y='Value',

        color='Stock'

    )


    fig2.update_layout(

        template='plotly_dark'

    )


    st.plotly_chart(

        fig2,

        use_container_width=True

    )



####################################################
# Candlestick Chart
####################################################

import yfinance as yf
import plotly.graph_objects as go


st.header(

"📈 Live Candlestick Chart"

)


stock_tv = st.selectbox(

"Choose Stock",

portfolio['Stock'].tolist(),

key="tv"

)



hist = yf.download(

f"{stock_tv}.NS",

period="6mo",

auto_adjust=False

)



if hist.empty:


    st.warning(

    "No historical data found."

    )


else:



    if isinstance(

        hist.columns,

        pd.MultiIndex

    ):



        hist.columns = hist.columns.get_level_values(0)




    fig = go.Figure()




    fig.add_trace(

        go.Candlestick(

            x=hist.index,


            open=hist["Open"],


            high=hist["High"],


            low=hist["Low"],


            close=hist["Close"],


            name=stock_tv

        )

    )




    fig.update_layout(


        template="plotly_dark",


        height=650,


        title=f"{stock_tv} Candlestick Chart",


        xaxis_rangeslider_visible=False


    )



    st.plotly_chart(


        fig,


        use_container_width=True


    )

###################################################
# Price Comparison
###################################################

st.subheader(

    "Price Comparison"

)

fig = px.bar(

    portfolio,

    x='Stock',

    y='Price',

    color='Stock',

    text='Price'

)



###################################################
# Second Row Charts
###################################################

col3, col4 = st.columns(2)


with col3:


    st.subheader(

        "Price Comparison"

    )


    fig3 = px.line(

        portfolio,

        x='Stock',

        y='Price',

        markers=True

    )


    st.plotly_chart(

        fig3,

        use_container_width=True

    )



with col4:


    st.subheader(

        "Quantity Distribution"

    )


    fig4 = px.bar(

        portfolio,

        x='Stock',

        y='Quantity',

        color='Stock',

        text='Quantity'

    )


    fig4.update_traces(

        textposition='outside'

    )


    st.plotly_chart(

        fig4,

        use_container_width=True

    )



###################################################
# Dynamic Sector Allocation
###################################################


sectors=[]


industries=[]


betas=[]


marketcaps=[]


countries=[]


dividends=[]



for stock in portfolio['Stock']:



    info = get_company_info(

        stock

    )



    sectors.append(

        info['Sector']

    )



    industries.append(

        info['Industry']

    )



    betas.append(

        info['Beta']

    )



    marketcaps.append(

        info['MarketCap']

    )



    countries.append(

        info['Country']

    )



    dividends.append(

        info['DividendYield']

    )




portfolio['Sector'] = sectors


portfolio['Industry'] = industries


portfolio['Beta'] = betas


portfolio['MarketCap'] = marketcaps


portfolio['Country'] = countries


portfolio['Dividend Yield'] = dividends

st.header(

"Sector Allocation"

)



sector_fig = px.pie(

portfolio,

names='Sector',

values='Value',

hole=0.4

)



sector_fig.update_layout(

template='plotly_dark',

height=600

)



st.plotly_chart(

sector_fig,

use_container_width=True

)


###################################################
# AI Portfolio Doctor
###################################################

st.header(

"AI Portfolio Doctor"

)


for _, row in portfolio.iterrows():

    if row['Confidence'] < 50:

        st.warning(

            f"{row['Stock']} has low confidence."

        )


    elif row['Confidence'] < 70:

        st.info(

            f"{row['Stock']} requires monitoring."

        )


    else:

        st.success(

            f"{row['Stock']} looks fundamentally strong."

        )


###################################################
# AI Suggested Rebalancing
###################################################

st.header(

"AI Suggested Rebalancing"

)


equity_weight = (

portfolio[

portfolio['Asset Class']=="Equity"

]['Value'].sum()

/

portfolio['Value'].sum()

)*100



if risk=="Low":

    target = 40


elif risk=="Medium":

    target = 65


else:

    target = 85




difference = equity_weight-target




c1,c2 = st.columns(2)



c1.metric(

"Current Equity",

f"{round(equity_weight,1)} %"

)



c2.metric(

"Target Equity",

f"{target}%"

)




if difference>10:


    st.warning(

f"Reduce Equity Exposure by {round(difference,1)}%"

)


elif difference<-10:


    st.info(

f"Increase Equity Exposure by {round(abs(difference),1)}%"

)


else:


    st.success(

"Portfolio Allocation is Optimal"

)




###################################################
# Market News Sentiment
###################################################

st.header(

    "Market News Sentiment"

)



st.info(

    "News sentiment indicates whether recent news flow around a company is favourable, neutral or unfavourable."

)



for _, row in portfolio.iterrows():



    if row['Sentiment'] == "Positive":



        st.success(

            f"{row['Stock']} : Positive"

        )



    elif row['Sentiment'] == "Neutral":



        st.info(

            f"{row['Stock']} : Neutral"

        )

    
    else:

        st.error(

            f"{row['Stock']} : Negative"

        )

###################################################
# AI Recommendations
###################################################

st.header(

    "AI Recommendations"

)


st.dataframe(

    portfolio[

        [

            'Stock',

            'Price',

            'Recommendation',

            'Confidence'

        ]

    ],

    use_container_width=True

)



###################################################
# Mini Bloomberg Terminal
###################################################

st.header(

    "Mini Bloomberg Terminal"

)


info={


'price':portfolio.loc[


portfolio['Stock']==stock,


'Price'


].iloc[0],



'beta':1,


'eps':15


}



a,b,c = st.columns(

    3

)


a.metric(

    "Price",

    round(

        info['price'],

        2

    )

)


b.metric(

    "EPS",

    round(

        info['eps'],

        2

    )

)


c.metric(

    "Beta",

    round(

        info['beta'],

        2

    )

)




###################################################
# Suggested Watchlist
###################################################

st.header(

    "Suggested Watchlist"

)


watchlist=[]


for _, row in portfolio.iterrows():

    if row['Confidence'] > 70:

        watchlist.append(

            row['Stock']

        )



if watchlist:

    st.success(

        ", ".join(

            watchlist

        )

    )


else:


    st.warning(

        "No stocks satisfy watchlist criteria."

    )



###################################################
# Top Holdings
###################################################

st.header(

    "Top Holdings"

)


ranking = portfolio.sort_values(

    'Value',

    ascending=False

)


st.dataframe(

    ranking,

    use_container_width=True

)



###################################################
# Download CSV
###################################################

csv = portfolio.to_csv(

    index=False

)


st.download_button(

    "📥 Download Portfolio CSV",

    csv,

    "portfolio.csv",

    "text/csv"

)



###################################################
# Dashboard Statistics
###################################################

st.header(

    "Dashboard Statistics"

)


x1,x2,x3 = st.columns(

    3

)


x1.metric(

    "Analysed Stocks",

    len(

        portfolio

    )

)

probability = portfolio['Confidence'].std()

x2.metric(

    "Average Confidence",

    round(

        portfolio['Confidence'].mean(),

        2

    )

)


x3.metric(

    "Average Volatility",

    round(

        probability,

        2

    )

)



###################################################
# Footer
###################################################

st.caption(

    "FinSight 2.0 | AI Powered Portfolio Analytics Platform"

)


st.caption(

    "Developed using Python, Streamlit, Yahoo Finance, Monte Carlo Simulation and AI Recommendation Engine"

)
