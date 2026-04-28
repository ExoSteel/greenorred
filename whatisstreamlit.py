import streamlit as st
import matplotlib.pyplot as plt
import json, os
from aquarel import load_theme
from dotenv import load_dotenv
import pandas as pd
from google import genai

load_dotenv()
st.set_page_config(layout="wide")

theme = load_theme("gruvbox_dark")
theme.apply()

with open("tickers.txt", "rt") as infile:
    data = infile.readlines()
    quotes = [d.strip("\n") for d in data]

selected_quote = st.sidebar.selectbox("Choose a quote:", quotes)

st.title(selected_quote)

with open(f"./predictions/predictions_{selected_quote}.txt", "rt") as infile:
    data = json.loads(infile.read())

positives = 0
negatives = 0
neutrals = 0
for d in data:
    if d['label'] == "positive":
        positives += 1
    elif d['label'] == "negative":
        negatives += 1
    else:
        neutrals += 1

COL1, COL2 = st.columns(2)

with COL1:
    st.subheader("General Sentiment")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Positives: " + str(positives))
    with col2:
        st.write("Negatives: " + str(negatives))
    with col3:
        st.write("Neutrals: " + str(neutrals))

    # 1. Prepare data
    labels = ["Positive", "Negative", "Neutral"]
    sizes = [positives, negatives, neutrals]

    # 2. Create the figure and axes
    fig, ax = plt.subplots(figsize=(10, 5))

    # 3. Generate the pie chart
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    theme.apply_transforms()

    st.pyplot(fig)
with COL2:
    st.subheader("Stock Price")
    df = pd.read_csv(f"./daily/daily_{selected_quote}.csv")

    # Convert 'date' column to actual datetime objects
    df['date'] = pd.to_datetime(df['date'])

    fig = plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['1. open'])

    # I'm gay. This makes the dates look pretty automatically
    plt.gcf().autofmt_xdate() 
    st.pyplot(fig)

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
