import streamlit as st
from modules.helper import readTicker, addTicker, readCandle, readPredictions, readOverview, readOptionsChain, readBBands, readFearAndGreed
from modules.alphaVantageAPI import getOverview, saveOverview, getBBands, saveBBands
from modules.yFinanceAPI import getNews, saveNews, getCandles, saveCandles, getOptionsChain, saveOptionsChain
from modules.finBertting import getPrediction, savePrediction
from modules.fearAndGreed import getFearAndGreed, saveFearAndGreed
from modules.technicals import monteCarloSimul, getSharpeRatio
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta, timezone
# from google import genai

red = "#8C0027"
darkred = "#380010"
orange = "#DD4111"
yellow = "#F1A512"
blue = "#A1D4B1" 
purple = "#653993"
green = "#2BAF90"
darkgreen = "#165a4a"
white = "#FFFCC7"
backgroundColor = "#000a13"

load_dotenv()
st.set_page_config(layout="wide")

if "timeframe" not in st.session_state:
    st.session_state.timeframe = "1M"

tickers = readTicker()
fng = readFearAndGreed()

def fearAndGreedTile(fng):
    st.sidebar.divider()
    # st.sidebar.title("Fear & Greed Index")
    # st.sidebar.write(f"{fng["fear_and_greed"]["score"]:.2f}")

    fng_score = fng["fear_and_greed"]["score"]

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = fng_score,
        title = {'text': "Fear & Greed Index"},
        # delta = {'reference': 10},
        gauge = {'axis': {'range': [None, 100]},
                'steps' : [
                    {'range': [0, 20], 'color': darkred},
                    {'range': [20, 40], 'color': red},
                    {'range': [40, 60], 'color': "grey"},
                    {'range': [60, 80], 'color': green},
                    {'range': [80, 100], 'color': darkgreen}
                ],
                'bar': {'color': white},
            }
        )
    )

    st.sidebar.plotly_chart(fig)

selected_ticker = st.sidebar.selectbox("Choose a quote:", tickers)
new_ticker = st.sidebar.text_input("Add a new ticker:")
fearAndGreedTile(fng)

if new_ticker != "":
    addTicker(new_ticker)

    news = getNews(new_ticker)
    saveNews(new_ticker, news)

    prediction = getPrediction(new_ticker)
    savePrediction(new_ticker, prediction)

    candles = getCandles(new_ticker)
    saveCandles(new_ticker, candles)

    calls_df, puts_df = getOptionsChain(new_ticker)
    saveOptionsChain(new_ticker, calls_df, puts_df)

    bbands = getBBands(new_ticker)
    saveBBands(new_ticker, bbands)

    new_ticker = ""
    selected_ticker = "AAPL"
    st.rerun()

preds = readPredictions(selected_ticker)
candles = readCandle(selected_ticker)
# print(df.head(5))


def titleTile(df):
    col1, col2, col3 = st.columns([1,10,1], vertical_alignment="center")
    with col1:
        st.title(selected_ticker)
        # st.markdown(f"<h1 style='justify-self:center;'>${selected_ticker}</h1>", unsafe_allow_html=True)
    with col2:
        try:
            ticker_current_price = df.iloc[-1]['Close']
            st.subheader(f"${ticker_current_price:.2f}")
            # st.markdown(f"<h3 style='color:{white};'>${ticker_current_price:.2f}</h3>", unsafe_allow_html=True)
        except:
            ticker_current_price = None
            pass
    with col3:
        if st.button("Refresh"):
            data = getCandles(selected_ticker)
            if data is not None:
                saveCandles(selected_ticker, data)
            # print(data)

            data, meta = getOverview(selected_ticker)
            if data is not None and meta is not None:
                saveOverview(selected_ticker, data)
            # print(data)

            calls_df, puts_df = getOptionsChain(selected_ticker)
            if calls_df is not None and puts_df is not None:
                saveOptionsChain(selected_ticker, calls_df, puts_df)

            fng = getFearAndGreed()
            if type(fng) == dict:
                saveFearAndGreed(fng)

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
    
    st.plotly_chart(fig, width="stretch")

def chartTile(ticker, df):
    timeframe = st.session_state.timeframe

    try:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df['rolling200'] = df['Close'].rolling(200).mean()
        df['rolling50'] = df['Close'].rolling(50).mean()
        df['rolling20'] = df['Close'].rolling(20).mean()

        bbands = readBBands(ticker)

        fig = go.Figure(data=[go.Candlestick(
            x = df['Date'],
            open = df['Open'],
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            name = "Price", 
            increasing_line_color = green, 
            decreasing_line_color = red
        )])

        fig.add_trace(go.Scatter(
            x = df["Date"],
            y = df['rolling200'],
            mode = "lines",
            name = "200 SMA",
            line = dict(color=orange, width=1)
        ))

        fig.add_trace(go.Scatter(
            x = df["Date"],
            y = df['rolling50'],
            mode = "lines",
            name = "50 SMA",
            line = dict(color=yellow, width=1)
        ))

        fig.add_trace(go.Scatter(
            x = df["Date"],
            y = df['rolling20'],
            mode = "lines",
            name = "20 SMA",
            line = dict(color=purple, width=1)
        ))

        if bbands is not None:
            fig.add_trace(go.Scatter(
                x=bbands["date"],
                y=bbands['Real Middle Band'],
                fill=None,
                mode='lines',
                line_color='rgba(255, 50, 50, 0.5)',
                line=dict(width=2),
                name='BB middle',
                # visible='legendonly'
            ))

            fig.add_trace(go.Scatter(
                x=bbands["date"],
                y=bbands['Real Upper Band'],
                fill=None,
                mode='lines',
                line_color='rgba(100, 100, 255, 0.5)',
                line=dict(width=2),
                name='BB upper',
                # visible='legendonly'
            ))

            fig.add_trace(go.Scatter(
                x=bbands["date"],
                y=bbands['Real Lower Band'],
                opacity=0.3,
                fill='tonexty',
                line=dict(width=2),
                name='BB lower',
                line_color='rgba(100, 100, 255, 0.5)',
                mode='lines', fillcolor='rgba(100, 100, 255, 0.1)',
                # visible='legendonly'
            ))

        today = datetime.now(timezone.utc)
        days = 31
        
        if timeframe == "1D":
            days = 1
        elif timeframe == "1W":
            days = 7
        elif timeframe == "1M":
            days = 31
        elif timeframe == "3M":
            days = 180
        elif timeframe == "1Y":
            days = 365
        else:
            days = (today - df["Date"].min()).days 

        delta = today - timedelta(days=days)
        upper, lower = df[df["Date"] >= delta].max()["High"] * 1.05, df[df["Date"] >= delta].min()["Low"] * 0.95

        fig.update_layout(
            xaxis=dict(
                range=[delta, today],
                type="date",
                rangebreaks=[
                    dict(bounds=["sat", "mon"]) # Hides everything between Saturday morning and Monday morning
                ]
            ),
            xaxis_rangeslider_visible=False,
            yaxis=dict(
                range=[lower, upper]
            ),
            legend=dict(
                orientation="v",
                yanchor="auto",
                y=1,
                xanchor="right",
                x=-0.05
            )
        )

        st.plotly_chart(fig, width="stretch")

        st.pills("Timeframe", ["1D", "1W", "1M", "3M", "1Y", "ALL"], default="1M", key="timeframe")

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
    with st.expander("Technicals", expanded=True):
        try:
            if ticker:
                # print("current", ticker_current_price)
                marginOS = (float(overview["AnalystTargetPrice"]) - float(ticker)) / float(ticker) * 100
                st.markdown(f"<h2 style='text-align: center;'>   {marginOS:.2f}%</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Margin of Safety</p>", unsafe_allow_html=True)

                sharpe_ratio = getSharpeRatio(candles)
                st.markdown(f"<h2 style='text-align: center;'>   {sharpe_ratio:.2f}%</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Sharpe Ratio</p>", unsafe_allow_html=True)

                technicalsTile(selected_ticker)
        except Exception as e:
            print(e)
            st.write("Data not found.")

def optionsChainTile(ticker):
    st.title("Options Chain")
    try:
        calls_df, puts_df = readOptionsChain(ticker)
        options_df = calls_df.merge(puts_df, on="strike")

        columns = pd.MultiIndex.from_tuples([
            ("CALLS", "Volume"),
            ("CALLS", "Last Price"),
            ("CALLS", "Bid"),
            ("CALLS", "Change"),
            ("STRIKE", ""),
            ("PUTS", "Change"),
            ("PUTS", "Bid"),
            ("PUTS", "Last Price"),
            ("PUTS", "Volume")
        ])

        headers = [
            "volume_x",
            "lastPrice_x",
            "bid_x",
            "change_x",
            "strike",
            "change_y",
            "volume_y",
            "lastPrice_y",
            "bid_y",
        ]
        
        custom_scale = [darkred, backgroundColor, darkgreen]
        
        min_strike = options_df['strike'].min()
        max_strike = options_df['strike'].max()
        strike_range = max_strike - min_strike if max_strike != min_strike else 1

        colorscale = pc.sample_colorscale(custom_scale, options_df.shape[0])

        options_df_trunc = options_df[headers]
        options_df_trunc.columns = columns
        options_df_trunc = options_df_trunc.fillna(0)

        def apply_row_gradient(x):
            return [f"background-color: {colorscale[i]}; color: white;" for i in range(len(x))]

        options_df_trunc = options_df_trunc.style.apply(
            apply_row_gradient, 
            subset=["STRIKE"],
            axis=0,
        )

        st.dataframe(options_df_trunc, hide_index=True, width="stretch")

    except Exception as e:
        st.write("Data not found")
        print(e)

def technicalsTile(ticker):
    candles = readCandle(ticker)
    overview = readOverview(ticker)

    SMA50 = overview["50DayMovingAverage"]
    MC_prices = monteCarloSimul(SMA50, 0.25, 0.5, n_sims=50000)

    fig = px.histogram(data_frame=MC_prices, title="Monte Carlo Simulation", color_discrete_sequence=[purple])

    fig.add_vline(
        x = MC_prices.mean(), 
        line_width = 4, 
        line_dash = "dash", 
        line_color = red,
        annotation_text=f"${MC_prices.mean():.2f}",
        annotation_position="top top"
    )

    st.plotly_chart(fig)


ticker_current_price = titleTile(candles)

st.divider()

COL1, COL2 = st.columns([3, 2])
with COL1:
    chartTile(selected_ticker, candles)
with COL2:
    sentimentTile(preds)

st.divider()

optionsChainTile(selected_ticker)

st.divider()

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