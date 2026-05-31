import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

S0 = 223.97        # Current price (from your 50-day average)
mu = 0.25          # expected annual return
sigma = 0.5       # annual volatility
T = 2              # Time horizon
dt = 1/262         # Time step (daily)
n_steps = 262
n_sims = 20000      # Number of "alternate universes"

# 2. Run the Simulation
shocks = np.random.normal(0, 1, (n_steps, n_sims))
price_paths = np.zeros_like(shocks)
price_paths[0] = S0

for t in range(1, n_steps):
    price_paths[t] = price_paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + 
                                               sigma * np.sqrt(dt) * shocks[t])
    
final_prices = price_paths[-1]
plt.hist(final_prices, bins=50, color='skyblue', edgecolor='black')

# Add labels
plt.axvline(final_prices.mean(), color='red', linestyle='dashed', linewidth=2, label='Mean')
plt.axvline(np.percentile(final_prices, 5), color='orange', linestyle='dotted', label='5th Percentile')
plt.axvline(np.percentile(final_prices, 95), color='orange', linestyle='dotted', label='95th Percentile')
plt.title("Distribution of Final Stock Prices")
plt.xlabel("Price ($)")
plt.ylabel("Frequency")

plt.show()
plt.savefig("./modules/test.png")
print(f"Mean: ${final_prices.mean():.2f} | 5th Percentile: ${np.percentile(final_prices, 5):.2f} | 95th Percentile: ${np.percentile(final_prices, 95):.2f}")