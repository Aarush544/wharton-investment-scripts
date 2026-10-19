import numpy as np
import yfinance as yf

PORTFOLIO_VALUE = 300000
EQUITY_SHARE = 0.7
NUM_STOCKS = 12
TYPICAL_VOL = 0.25
POSITION_CAP = 0.13

ticker = input("Enter ticker: ").upper()

data = yf.download(
    ticker,
    period="3y",
    interval="1d",
    auto_adjust=True,
    progress=False
)

if data.empty:
    raise SystemExit("No data found. Check the ticker.")

close = data["Close"].squeeze()

price = float(close.iloc[-1])
volatility = float(np.log(close).diff().dropna().std() * np.sqrt(252))

base_weight = EQUITY_SHARE/NUM_STOCKS

volatility_adjustment = TYPICAL_VOL/volatility
weight = base_weight * volatility_adjustment
weight = min(weight, POSITION_CAP * EQUITY_SHARE)


dollars = weight * PORTFOLIO_VALUE
shares = int(dollars / price)
position_value = shares * price


print("Shares:", shares)
print("Recommended Dollars Spent:", round(dollars, 2))
print("Possible Dollars Spent:", round(position_value, 2))
print(f"Weight: {weight:.2%}")
