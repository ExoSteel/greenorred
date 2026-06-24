import numpy as np
import pandas as pd
import scipy.stats as si
from scipy.optimize import fsolve
from datetime import datetime, timedelta, timezone

def monteCarloSimul(S0, mu, sigma, T=1, dt=1/262, n_steps=262, n_sims=10000):
    '''
    S0: Current price (from your 50-day average)
    mu: expected annual return
    sigma: annual volatility
    T: Time horizon
    dt: Time step (daily)
    n_sims: No. of simulations
    '''
    shocks = np.random.normal(0, 1, (n_steps, n_sims))
    price_paths = np.zeros_like(shocks)
    price_paths[0] = S0

    for t in range(1, n_steps):
        price_paths[t] = price_paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + 
                                                sigma * np.sqrt(dt) * shocks[t])
        
    final_prices = price_paths[-1]
    percentile5 = np.percentile(final_prices, 5)
    percentile95 = np.percentile(final_prices, 95)

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

    return final_prices, percentile5, percentile95

def __calculateGeometricReturns(df):
    pass

def __calculateLogReturns(df):
    return np.log(df["Adj Close"] / df["Adj Close"].shift(1))

def calculateCAPM(beta=0, E_Rm=0.1788, R_f=0.0367):
    '''
    beta: Beta
    E_Rm: S&P 500 Expected Market Returns (17.88%)
    R_f: US Risk-free Rate (3.67%)
    '''
    if not beta:
        return None
    
    MRP = E_Rm - R_f # Market Risk Premium
    scaled_prem = MRP * beta # Scaled Premium

    expected_returns = scaled_prem + R_f # Expected Market Return

    return expected_returns

def getBBands(df, N=20, K=2):
    # Middle Band
    df["Real Middle Band"] = df["Close"].rolling(window=N).mean()
    df['Standard Deviation'] = df['Close'].rolling(window=N).std()

    df['Real Upper Band'] = df['Real Middle Band'] + (K * df['Standard Deviation'])
    df['Real Lower Band'] = df['Real Middle Band'] - (K * df['Standard Deviation'])

    return df
    
def getPivot(high, low, close):
    pivot = (high + low + close) / 3
    return pivot

def getSupportLevel():
    pass

def getResistanceLevel(df):
    yest = df.iloc[-2]

    high = yest["High"]
    low = yest["Low"]
    close = yest["Close"]

    pivot = getPivot(high, low, close)

    R1 = (2 * pivot) - low
    R2 = pivot + (high - low)

    print(R1, R2)
    return R1, R2

def getSharpeRatio(df, period="1y", risk_free_rate=0.04):
    df['Date'] = pd.to_datetime(df['Date'], utc=True)

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

def calculatePCR(calls, puts):
    totalCalls = calls.sum()
    totalPuts = puts.sum()

    PCR = totalPuts / totalCalls if totalCalls > 0 else 0
    return totalCalls, totalPuts, PCR

# def calculateBlackScholesCall(S, K, T, r, sigma):
#     d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
#     d2 = d1 - sigma * np.sqrt(T)
#     call_price = S * si.norm.cdf(d1) - K * np.exp(-r * T) * si.norm.cdf(d2)
#     return call_price

# def calculateIV(price, S, K, T, r):
#     func = lambda sigma: calculateBlackScholesCall(S, K, T, r, sigma) - price
    
#     initial_guess = 0.20
#     iv = fsolve(func, initial_guess)[0]
#     return iv

def calculateVolatility(df):
    df['Date'] = pd.to_datetime(df['Date'], utc=True)

    today = datetime.now(timezone.utc)
    delta = today - timedelta(days=365)

    df = df[df["Date"] >= delta]
    df["log_return"] = __calculateLogReturns(df)

    daily_volatility = df["log_return"].std()
    annual_volatility = daily_volatility * np.sqrt(252)

    return annual_volatility

if __name__ == "__main__":
    # S = 348.78      # Stock Price
    # K = 350.00      # Strike Price
    # T = 3 / 365    # 30 days to expiration
    # r = 0.0367      # 5% risk-free rate
    # C_market = 4.88 # Current Call market price

    # iv = calculateIV(C_market, S, K, T, r)
    # print(f"Implied Volatility: {iv * 100:.2f}%")

    print(calculateCAPM(1.22))