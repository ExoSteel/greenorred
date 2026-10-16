import streamlit as st
from .api.helper import readPredictions
from .constants import *

def sentimentAnalysis(ticker):

    try:
        preds = readPredictions(ticker)

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
    except Exception as e:
        st.write("Data not found.")
        print(
            e,
            "\n", type(e).__name__,
            "\n Filename:", __file__,         
            "\n Line:", e.__traceback__.tb_lineno
        )