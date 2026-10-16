import os
import streamlit as st
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
 
from backtesting.test import SMA, GOOG

class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 50)
        self.ma2 = self.I(SMA, price, 200)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


bt = Backtest(GOOG, SmaCross, commission=.002,
              exclusive_orders=True, finalize_trades=True)
stats = bt.run()

plot_filename = "./backtesting_plots/backtest_plot.html"
bt.plot(filename=plot_filename, open_browser=False)

if os.path.exists(plot_filename):
    with open(plot_filename, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.iframe(html_content, height=700)

st.write(stats)