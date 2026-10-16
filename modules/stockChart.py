import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from .constants import *
from .api.helper import readCandles
from .technicals import getBBands

def stockChart(ticker, timeframe):
    try:
        df = readCandles(ticker)

        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df['rolling20'] = df['Close'].rolling(20).mean()
        df['rolling50'] = df['Close'].rolling(50).mean()
        df['rolling200'] = df['Close'].rolling(200).mean()

        fig = go.Figure(data=[
            go.Candlestick(
                x = df['Date'],
                open = df['Open'],
                high = df['High'],
                low = df['Low'],
                close = df['Close'],
                name = "Candles", 
                increasing_line_color = green, 
                decreasing_line_color = red,
                visible='legendonly'
                )
            ]
        )

        fig.add_trace(go.Scatter(
            x = df["Date"],
            y = df["Close"],
            name = "Close",
            line = dict(color=green, width=2)
            )
        )

        fig.add_trace(go.Scatter(
            x = df["Date"],
            y = df['rolling200'],
            mode = "lines",
            name = "200 SMA",
            line = dict(color=orange, width=1)
            )
        )

        fig.add_trace(go.Scatter(
            x = df["Date"],
            y = df['rolling50'],
            mode = "lines",
            name = "50 SMA",
            line = dict(color=yellow, width=1)
            )
        )

        # fig.add_trace(go.Scatter(
        #     x = df["Date"],
        #     y = df['rolling20'],
        #     mode = "lines",
        #     name = "20 SMA",
        #     line = dict(color=purple, width=1)
        #     )
        # )

        # R1, R2 = getResistanceLevel(df)

        # fig.add_hline(
        #     y = R1,
        #     line_color = 'rgba(255, 0, 0, 0.75)',
        #     name = "Resist 1"
        # )

        # fig.add_hline(
        #     y = R2,
        #     line_color = 'rgba(255, 0, 0, 0.75)',
        #     name = "Resist 2"
        # )
        
        df = getBBands(df)

        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df['Real Middle Band'],
            fill=None,
            mode='lines',
            line_color='rgba(255, 50, 50, 0.5)',
            line=dict(width=2),
            name='BB middle',
            # visible='legendonly'
        ))

        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df['Real Upper Band'],
            fill=None,
            mode='lines',
            line_color='rgba(100, 100, 255, 0.5)',
            line=dict(width=2),
            name='BB upper',
            # visible='legendonly'
        ))

        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df['Real Lower Band'],
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
        print(
            e,
            "\n", type(e).__name__,
            "\n Filename:", __file__,         
            "\n Line:", e.__traceback__.tb_lineno
        )