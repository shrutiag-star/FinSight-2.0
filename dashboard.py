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

current_time=datetime.now()

st.info(

f"⏱ Last Updated : {current_time.strftime('%H:%M:%S')}"

)


###################################################
# Title
###################################################

st.title(

    "📈 FinSight 2.0"

)


st.subheader(

    "AI Powered Portfolio Dashboard"

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



####################################################
# AI Portfolio Generator
####################################################

st.header(

    "AI Suggested Portfolio"

)

if risk=="Low":


    suggested={


        'HDFCBANK':40,

        'TCS':30,

        'ITC':20,

        'GOLDBEES':10


    }

elif risk=="Medium":


    suggested={


        'RELIANCE':30,

        'TCS':30,

        'BAJFINANCE':20,

        'NIFTYBEES':20


    }



else:


    suggested={


        'RELIANCE':25,

        'DIXON':25,

        'TATAMOTORS':25,

        'ZOMATO':25


    }




invest=pd.DataFrame(


{

'Stock':suggested.keys(),

'Allocation %':suggested.values()

}


)

invest['Amount']=(

invest['Allocation %']

*

capital

/

100

).round(0)


st.dataframe(


invest,


use_container_width=True


)



st.header(

"SIP Planner"

)


sip=st.number_input(

"Monthly SIP",

1000,

100000,

10000

)



r=0.12/12

n=years*12


future=sip*((1+r)**n-1)/r


future=round(

future,

0

)



st.metric(

"Expected Corpus",

f"₹{round(future,0)}"

)



st.header(

"Retirement Planner"

)



age=st.slider(

"Current Age",

20,

60,

25

)



retire=st.slider(

"Retirement Age",

55,

70,

60

)



expense=st.number_input(

"Monthly Expense",

10000,

500000,

50000

)



inflation=0.06


yrs=retire-age



corpus=(


expense*12*25


)*(


1+inflation


)**yrs


corpus=round(

corpus,

0

)



st.metric(

"Required Corpus",

f"₹{round(corpus/10000000,2)} Cr"

)


###################################################
# Time
###################################################

current_time = datetime.now().currftime(

    "%d-%m-%Y %H:%M:%S"

)


st.info(

    f"🕒 Current Time : {current_time}"

)



###################################################
# Upload Portfolio
###################################################

uploaded = st.file_uploader(

    "Upload Portfolio",

    type=['csv']

)


if uploaded:


    portfolio = pd.read_csv(

        uploaded

    )


    portfolio.columns = [

        x.strip()

        for x in portfolio.columns

    ]


    rename = {

        'Company': 'Stock',

        'Shares': 'Quantity',

        'Units': 'Quantity'

    }


    portfolio.rename(

        columns=rename,

        inplace=True

    )


    required = {

        'Stock',

        'Quantity'

    }


    if not required.issubset(

        portfolio.columns

    ):


        st.error(

            "CSV must contain Stock and Quantity columns"

        )


        st.stop()


    portfolio['Stock'] = portfolio['Stock'].astype(

        str

    )


    portfolio['Quantity'] = pd.to_numeric(

        portfolio['Quantity'],

        errors='coerce'

    )


    portfolio.dropna(

        inplace=True

    )


else:


    import os


    path = os.path.join(

        os.getcwd(),

        'portfolio.csv'

    )


    portfolio = pd.read_csv(

        path

    )


    portfolio['Stock'] = portfolio['Stock'].astype(

        str

    )


    portfolio['Quantity'] = pd.to_numeric(

        portfolio['Quantity'],

        errors='coerce'

    )


    portfolio.dropna(

        inplace=True

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



    data = get_data(

        row['Stock']

    )



    price = data['price']

    beta = data['beta']



    prices.append(

        price

    )



    news = sentiment()



    sentiments.append(

        news

    )



    if beta < 1:



        recommendations.append(

            "BUY"

        )



        confidence.append(

            80

        )



    elif beta < 1.3:



        recommendations.append(

            "HOLD"

        )



        confidence.append(

            65

        )



    else:



        recommendations.append(

            "SELL"

        )



        confidence.append(

            40

        )



analysis_end = time.time()



analysis_time = round(

    analysis_end

    -

    analysis_start,

    2

)



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


portfolio['Confidence'] = confidence


portfolio['Sentiment'] = sentiments




###################################################
# Timer
###################################################

st.success(

    f"⏱ Analysis Time : {analysis_time} sec"

)



###################################################
# Holdings
###################################################

st.header(

    "Portfolio Holdings"

)



st.dataframe(

    portfolio,

    use_container_width=True

)



###################################################
# Summary
###################################################

st.header(

    "Portfolio Summary"

)



c1,c2,c3,c4,c5 = st.columns(

    5

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



largest = portfolio.loc[


    portfolio['Value'].idxmax()


]



c5.metric(

    "Largest Holding",

    largest['Stock']

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



st.metric(

"FinSight AI Score",

score

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

col1, col2 = st.columns(2)


with col1:


    st.subheader(

        "Portfolio Allocation"

    )


    fig1 = px.pie(

        portfolio,

        names='Stock',

        values='Value',

        hole=0.4

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

        color='Stock',

        text='Value'

    )


    fig2.update_traces(

        textposition='outside'

    )


    st.plotly_chart(

        fig2,

        use_container_width=True

    )



####################################################
# Live Candlestick Chart
####################################################

import yfinance as yf
import plotly.graph_objects as go

st.subheader(

"📈 Live Candlestick Chart"

)

stock_tv = st.selectbox(

"Choose Stock",

portfolio['Stock'].tolist(),

key='tv'

)


hist = yf.download(

f"{stock_tv}.NS",

period="6mo"

)


fig = go.Figure(

data=[

go.Candlestick(

x=hist.index,

open=hist['Open'],

high=hist['High'],

low=hist['Low'],

close=hist['Close']

)

]

)


fig.update_layout(

template="plotly_dark",

height=700,

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
# Sector Allocation
###################################################

if 'Sector' not in portfolio.columns:


portfolio['Sector']='Others'


if 'Sector' in portfolio.columns:


    st.header(

        "Sector Allocation"

    )


    sector_fig = px.pie(

        portfolio,

        names='Sector',

        values='Value',

        hole=0.4

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
# Portfolio Rebalancing Advisor
###################################################

st.header(

    "Portfolio Rebalancing Advisor"

)



largest_weight = (

    largest['Value']

    /

    portfolio['Value'].sum()

) * 100



if largest_weight > 40:



    st.warning(

        f"{largest['Stock']} contributes "

        f"{round(largest_weight,2)}% "

        "of portfolio."

    )



    st.info(

        "Suggested Action : Reduce exposure "

        "and diversify holdings."

    )



else:



    st.success(

        "Portfolio allocation appears balanced."

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
# Monte Carlo Simulation
###################################################

st.header(

    "Monte Carlo Simulation"

)


st.info(

"Monte Carlo Simulation predicts future stock prices by analysing thousands of possible market movements."

)


if info['price'] > 0:

    minimum, average, maximum, probability = monte_carlo(

        info['price']

    )

else:

    minimum = 0
    average = 0
    maximum = 0
    probability = 0


mc = pd.DataFrame(

    {

        'Scenario':[

            'Minimum',

            'Average',

            'Maximum'

        ],


        'Price':[

            minimum,

            average,

            maximum

        ]

    }

)


fig_mc = px.bar(

    mc,

    x='Scenario',

    y='Price',

    color='Scenario',

    text='Price'

)


fig_mc.update_traces(

    textposition='outside'

)


st.plotly_chart(

    fig_mc,

    use_container_width=True

)


st.success(

    f"Probability of Gain : {round(probability,2)} %"

)



###################################################
# Suggested Watchlist
###################################################

st.header(

    "Suggested Watchlist"

)


watchlist = []


for _,row in portfolio.iterrows():


    if row['Confidence'] >= 70:


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
