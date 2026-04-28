import streamlit as st
from modules.helper import readTicker, addTicker, readCandle, readPredictions, readOverview
from modules.alphaVantageAPI import getCandle, saveCandle, getOverview, saveOverview, getBBands
from modules.yFinanceAPI import getNews, saveNews
from modules.finBertting import getPrediction, savePrediction
import matplotlib.pyplot as plt
from aquarel import load_theme
from dotenv import load_dotenv
import pandas as pd
from google import genai
import os

tickers = readTicker()

# data = getBBands("MSFT")
# data.plot()
# plt.title(f'BBbands indicator for {ticker} stock (60 min)')
# plt.show()

load_dotenv()
st.set_page_config(layout="wide")

# theme = load_theme("gruvbox_dark")
# theme.apply()

selected_ticker = st.sidebar.selectbox("Choose a quote:", tickers)
new_ticker = st.sidebar.text_input("Add a new ticker:")
# print("New ticker:", new_ticker)

if new_ticker != "":
    addTicker(new_ticker)
    news = getNews(new_ticker)
    saveNews(new_ticker, news)

    prediction = getPrediction(new_ticker)
    savePrediction(new_ticker, prediction)

    new_ticker = ""
    selected_ticker = "AMZN"
    st.rerun()

preds = readPredictions(selected_ticker)

col1, col2 = st.columns([5,1])
with col1:
    st.title(selected_ticker)
with col2:
    if st.button("Refresh"):
        data, meta = getCandle(selected_ticker)
        saveCandle(selected_ticker, data)
        print(data)

        data, meta = getOverview(selected_ticker)
        saveOverview(selected_ticker, data)
        print(data)


COL1, COL2 = st.columns(2)

with COL1:
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

    labels = ["Positive", "Negative", "Neutral"]
    sizes = [positives, negatives, neutrals]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    # theme.apply_transforms()

    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Positives: " + str(positives))
    with col2:
        st.write("Negatives: " + str(negatives))
    with col3:
        st.write("Neutrals: " + str(neutrals))
with COL2:
    st.subheader("Stock Price")
    try:
        df = readCandle(selected_ticker)

        df['date'] = pd.to_datetime(df['date'])

        fig = plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['1. open'])
        plt.gcf().autofmt_xdate() 
        st.pyplot(fig)
    except:
        st.write("Data not found.")

with st.expander("Overview", expanded=True):

    with st.container():
        try:
            overview = readOverview(selected_ticker)
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
                "ExDividendDate",
                "RevenueTTM",
                "GrossProfitTTM",
                "DividendDate"
            ]

            analyst_tags = [
                "AnalystRatingStrongBuy",
                "AnalystRatingBuy",
                "AnalystRatingHold",
                "AnalystRatingSell",
                "AnalystRatingStrongSell"
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

                    st.markdown(f"<h2 style='text-align: center;'>   {value}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center;'>{key}</p>", unsafe_allow_html=True)
        except:
            st.write("Data not found.")

with st.expander("Analysis", expanded=False):
    pass

def chatbot():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    st.title("Echo Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = ""
    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    prompt += "\n Please keep it under 200 words \n"

    if prompt:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        ).text
    else:
        response = "Bum"

    with st.chat_message("assistant"):
        st.markdown(f"Echo: {response}")
    st.session_state.messages.append({"role": "assistant", "content": response})

# chatbot()