import numpy as np
import yfinance as yf

NUM_SIMULATIONS = 5000
TRADING_DAYS = 2520
ASSUMED_ANNUAL_RETURN = 0.08


ticker = input("Enter the ticker: ").upper()

close_prices = yf.download(
    ticker, 
    period="10y", 
    interval="1d", 
    auto_adjust=True, progress=False
)["Close"].to_numpy().flatten()

if close_prices.empty:
    raise SystemExit("No data found. Check the ticker.")

returns = np.diff(np.log(close_prices))
returns = returns - np.mean(returns)

daily_drift = np.log(1 + ASSUMED_ANNUAL_RETURN) / 252 - 0.5 * np.var(returns)

initial_price = float(close_prices[-1])

sampled_returns = np.random.choice(returns, size=(TRADING_DAYS, NUM_SIMULATIONS)) + daily_drift
daily_returns = np.exp(sampled_returns)

price_paths = initial_price * np.cumprod(
    np.vstack([np.ones(NUM_SIMULATIONS), daily_returns]), axis=0
)

terminal_values = price_paths[-1, :]
p5_outcome = np.percentile(terminal_values, 5)   # Worst 5% outcome
p95_outcome = np.percentile(terminal_values, 95) # Best 5% outcome

one_year_values = price_paths[252, :]
one_year_returns = (one_year_values - initial_price) / initial_price

var_1yr = np.percentile(one_year_returns, 5)
cvar_1yr = one_year_returns[one_year_returns <= var_1yr].mean()

print(f"\n--- Monte Carlo Results ---")
print(f"Starting Price:      ${initial_price:,.2f}")
print(f"Median 10-Yr Price:  ${np.median(terminal_values):,.2f}")
print(f"5th Percentile:      ${p5_outcome:,.2f}")
print(f"95th Percentile:     ${p95_outcome:,.2f}")
print(f"1-Year VaR:          {var_1yr:.2%}")
print(f"1-Year CVaR:         {cvar_1yr:.2%}")
print(f"Chance of Loss (1Y): {(one_year_returns < 0).mean():.1%}") 