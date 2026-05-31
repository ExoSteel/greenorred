import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

S0 = 223.97        # Current price (from your 50-day average)
mu = 0.25          # expected annual return
sigma = 0.5       # annual volatility
T = 1              # Time horizon
dt = 1/262         # Time step (daily)
n_steps = 262
n_sims = 20000      # Number of "alternate universes"

def monteCarloSimul(S0, mu, sigma, T=1, dt=1/262, n_steps=262, n_sims=10000):
    shocks = np.random.normal(0, 1, (n_steps, n_sims))
    price_paths = np.zeros_like(shocks)
    price_paths[0] = S0

    for t in range(1, n_steps):
        price_paths[t] = price_paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + 
                                                sigma * np.sqrt(dt) * shocks[t])
        
    final_prices = price_paths[-1]
    # plt.hist(final_prices, bins=50, color='skyblue', edgecolor='black')

    # Add labels
    # plt.axvline(final_prices.mean(), color='red', linestyle='dashed', linewidth=2, label='Mean')
    # plt.axvline(np.percentile(final_prices, 5), color='orange', linestyle='dotted', label='5th Percentile')
    # plt.axvline(np.percentile(final_prices, 95), color='orange', linestyle='dotted', label='95th Percentile')
    # plt.title("Distribution of Final Stock Prices")
    # plt.xlabel("Price ($)")
    # plt.ylabel("Frequency")

    # plt.savefig("./modules/test.png")
    # print(f"Mean: ${final_prices.mean():.2f} | 5th Percentile: ${np.percentile(final_prices, 5):.2f} | 95th Percentile: ${np.percentile(final_prices, 95):.2f}")

    return final_prices

def getPivot(high, low, close):
    pivot = (high + low + close) / 3
    return pivot

def getSupportLevel():
    pass

def getResistanceLevel(pivot, low):
    R1 = (2 * pivot) / low
    return R1

def getSharpeRatio(df, period="1y", risk_free_rate=0.04):
    if period == "5y":
        days = 365 * 5
    elif period == "5y":
        days = 365 * 10
    else:
        days = 365
    
    today = datetime.now(timezone.utc)
    delta = today - timedelta(days=days)

    df = df[df["Date"] >= delta]

    # print(df)
    df["Daily Return"] = df["Close"].pct_change()

    avg_daily_return = df['Daily Return'].mean()
    daily_volatility = df['Daily Return'].std()
    
    annualized_return = avg_daily_return * 252
    annualized_volatility = daily_volatility * np.sqrt(252)
    
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    
    # print(f"Annualized Return:     {annualized_return*100:.2f}%")
    # print(f"Annualized Volatility: {annualized_volatility*100:.2f}%")
    # print(f"Sharpe Ratio:          {sharpe_ratio:.2f}")

    return sharpe_ratio

if __name__ == "__main__":
    pass