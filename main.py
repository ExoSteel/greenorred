import streamlit as st
from modules.helper import readTicker, addTicker, readCandle, readPredictions, readOverview
from modules.alphaVantageAPI import getOverview, saveOverview, getBBands
from modules.yFinanceAPI import getNews, saveNews, getCandles, saveCandles, getOptionsChain
from modules.finBertting import getPrediction, savePrediction
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv
import pandas as pd
# from google import genai

red = "#8C0027"
orange = "#DD4111"
yellow = "#F1A512"
blue = "#A1D4B1" 
green = "#2BAF90"
white = '#FFFCC7'

load_dotenv()
st.set_page_config(layout="wide")

tickers = readTicker()
selected_ticker = st.sidebar.selectbox("Choose a quote:", tickers)
new_ticker = st.sidebar.text_input("Add a new ticker:")

if new_ticker != "":
    addTicker(new_ticker)
    news = getNews(new_ticker)
    saveNews(new_ticker, news)

    prediction = getPrediction(new_ticker)
    savePrediction(new_ticker, prediction)

    candles = getCandles(new_ticker)
    saveCandles(new_ticker, candles)

    new_ticker = ""
    selected_ticker = "AAPL"
    st.rerun()

preds = readPredictions(selected_ticker)
candles = readCandle(selected_ticker)
# print(df.head(5))


def titleTile(df):
    col1, col2, col3 = st.columns([1,5,1])
    with col1:
        st.markdown(f"<h1>${selected_ticker}</h1>", unsafe_allow_html=True)
    with col2:
        try:
            ticker_current_price = df.iloc[-1]['Close']
            st.markdown(f"<h2>${ticker_current_price:.2f}</h2>", unsafe_allow_html=True)
        except:
            ticker_current_price = None
            pass
    with col3:
        if st.button("Refresh"):
            data = getCandles(selected_ticker)
            saveCandles(selected_ticker, data)
            # print(data)

            data, meta = getOverview(selected_ticker)
            saveOverview(selected_ticker, data)
            # print(data)

    return ticker_current_price

def sentimentTile(preds):
    st.subheader("General Sentiment")

    positives = 0
    negatives = 0
    neutrals = 0
    for pred in preds:
        if pred['label'] == "positive":
            positives += 1
        elif pred['label'] == "negative":
            negatives += 1
        else:
            neutrals += 1

    labels = ["Positive", "Neutral", "Negative"]
    sizes = [positives, neutrals, negatives ]

    fig = px.pie(
        values=sizes, 
        names=labels,
        color=labels,
        color_discrete_map={
            'Positive' : green,
            'Neutral' : white,
            'Negative' : red,
            }
    )

    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="auto",
            y=1,
            xanchor="right",
            x=0.2
        )
    )
    
    st.plotly_chart(fig, width="stretch")

def chartTile(df):
    print(df.tail(5))
    st.subheader("Stock Price")
    try:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df['rolling200'] = df['Open'].rolling(200).mean()
        df['rolling50'] = df['Open'].rolling(50).mean()
        
        # mask = (df['Date'] > '2025-01-01') & (df['Date'] <= '2026-05-04')
        # df = df.loc[mask]

        fig = go.Figure(data=[go.Candlestick(
            x = df['Date'],
            open = df['Open'],
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            increasing_line_color = green, 
            decreasing_line_color = red
        )])

        fig.add_trace(go.Scatter(
            x = df["Date"],
            y = df['rolling200'],
            mode = "lines",
            name = "200 SMA",
            line = dict(color=orange, width=2)
        ))

        fig.add_trace(go.Scatter(
            x = df["Date"],
            y = df['rolling50'],
            mode = "lines",
            name = "50 SMA",
            line = dict(color=yellow, width=2)
        ))

        fig.update_layout(
            xaxis_rangeslider_visible=False,
            margin=dict(l=10, r=10, t=10, b=10),
            template="plotly_dark" # Matches dark themes nicely
        )

        st.plotly_chart(fig, width="stretch")

    except Exception as e:
        st.write("Data not found.")
        print(e)

def overviewTile(ticker):
    with st.expander("Overview", expanded=True):
        with st.container():
            try:
                overview = readOverview(ticker)
                # print(overview)

                desc_tags = [
                    "Symbol",
                    "AssetType",
                    "Name",
                    "Description",
                    "CIK",
                    "Exchange",
                    "Currency",
                    "Country",
                    "Sector",
                    "Industry",
                    "Address",
                    "OfficialSite",
                    "FiscalYearEnd",
                    "LatestQuarter",
                    "MarketCapitalization",
                    "EBITDA",
                    "SharesOutstanding",
                    "SharesFloat",
                    "PercentInstitutions",
                    "DividendData",
                    "DividendPerShare",
                    "DividendYield",
                    "ExDividendDate",
                    "RevenueTTM",
                    "GrossProfitTTM",
                    "DividendDate",
                    "ExDividendDate"
                ]

                analyst_tags = [
                    "AnalystRatingStrongBuy",
                    "AnalystRatingBuy",
                    "AnalystRatingHold",
                    "AnalystRatingSell",
                    "AnalystRatingStrongSell"
                ]

                percentage_tags = [
                    "ProfitMargin",
                    "OperatingMarginTTM",
                    "ReturnOnAssetsTTM",
                    "ReturnOnEquityTTM",
                    "QuarterlyEarningsGrowthYOY",
                    "QuarterlyRevenueGrowthYOY",
                    "PriceToSalesRatioTTM",
                    "PercentInsiders"
                ]

                st.markdown("<h3 style='text-align: center;'>   Analyst Ratings</h3>", unsafe_allow_html=True)
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.markdown(f"<h2 style='text-align: center;'>   {overview[analyst_tags[4]]}</h2>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: darkred;'>Strong Sell</p>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<h2 style='text-align: center;'>   {overview[analyst_tags[3]]}</h2>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: red'>Sell</p>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<h2 style='text-align: center;'>   {overview[analyst_tags[2]]}</h2>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: yellow'>Hold</p>", unsafe_allow_html=True)
                with col4:
                    st.markdown(f"<h2 style='text-align: center;'>   {overview[analyst_tags[1]]}</h2>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: green'>Buy</p>", unsafe_allow_html=True)
                with col5:
                    st.markdown(f"<h2 style='text-align: center;'>   {overview[analyst_tags[0]]}</h2>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: darkgreen'>Strong Buy</p>", unsafe_allow_html=True)


                with st.container():
                    for key, value in overview.items():
                        if key in desc_tags or key in analyst_tags:
                            continue
                        elif key in percentage_tags:
                            st.markdown(f"<h2 style='text-align: center;'>   {float(value)*100:.2f}%</h2>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align: center;'>{key}</p>", unsafe_allow_html=True)
                            continue
                        st.markdown(f"<h2 style='text-align: center;'>   {value}</h2>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center;'>{key}</p>", unsafe_allow_html=True)

                return overview
            except Exception as e:
                print(e)
                st.write("Data not found.")

def analysisTile(ticker, overview):
    with st.expander("Analysis", expanded=False):
        try:
            if ticker:
                # print("current", ticker_current_price)
                marginOS = (float(overview["AnalystTargetPrice"]) - float(ticker)) / float(ticker) * 100
                st.markdown(f"<h2 style='text-align: center;'>   {marginOS:.2f}%</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Margin of Safety</p>", unsafe_allow_html=True)
        except Exception as e:
            print(e)
            st.write("Data not found.")

def optionsChainTile(ticker):
    calls_df, puts_df = getOptionsChain(ticker)
    st.title("Options Chain")

    options_df = calls_df.merge(puts_df, on="strike")

    columns = pd.MultiIndex.from_tuples([
        ("CALLS", "Volume"),
        ("CALLS", "Last Price"),
        ("CALLS", "Bid"),
        ("STRIKE", ""),
        ("PUTS", "Bid"),
        ("PUTS", "Last Price"),
        ("PUTS", "Volume")
    ])

    headers = [
        "volume_x",
        "lastPrice_x",
        "bid_x",
        "strike",
        "volume_y",
        "lastPrice_y",
        "bid_y",
    ]

    options_df_trunc = options_df[headers]
    options_df_trunc.columns = columns

    options_df_trunc = options_df_trunc.fillna(0)
    st.dataframe(options_df_trunc, hide_index=True, width="stretch")

ticker_current_price = titleTile(candles)

COL1, COL2 = st.columns([2, 3])
with COL1:
    sentimentTile(preds)
with COL2:
    chartTile(candles)

optionsChainTile(selected_ticker)

col1, col2 = st.columns(2)
with col1:
    overview = overviewTile(selected_ticker)
with col2:
    analysisTile(ticker_current_price, overview)
    







# def chatbot():
#     client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
#     st.title("Echo Bot")

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     prompt = ""
#     if prompt := st.chat_input("What is up?"):
#         with st.chat_message("user"):
#             st.markdown(prompt)
#         st.session_state.messages.append({"role": "user", "content": prompt})

#     prompt += "\n Please keep it under 200 words \n"

#     if prompt:
#         response = client.models.generate_content(
#             model="gemini-3.1-flash-lite-preview",
#             contents=prompt
#         ).text
#     else:
#         response = "Bum"

#     with st.chat_message("assistant"):
#         st.markdown(f"Echo: {response}")
#     st.session_state.messages.append({"role": "assistant", "content": response})

# chatbot()