import pandas as pd
import numpy as np
import yfinance as yf

PORTFOLIO_VALUE = 300000
POSITION_CAP = 0.1
RISK_PER_TRADE = 0.005

ticker = input("Enter ticker: ")
df = yf.download(ticker, period="10y", interval="1d", auto_adjust=True, progress=False)
df["Daily_Returns"] = df["Close"].pct_change()

annual_volatility = df["Daily_Returns"].dropna().std() * np.sqrt(252)

high = df["High"].squeeze()
low = df["Low"].squeeze()
close = df["Close"].squeeze() 

previous_close = close.shift(1)

true_range = pd.concat([high - low, abs(high - previous_close), abs(low - previous_close)], axis=1).max(axis=1)

atr_history = true_range.rolling(window=14).mean()
atr = atr_history.iloc[-1]

returns = df["Daily_Returns"].dropna()

latest_price = np.asarray(df["Close"].iloc[-1]).item()
max_capital = PORTFOLIO_VALUE * POSITION_CAP
risk_amount = PORTFOLIO_VALUE * RISK_PER_TRADE

stop_distance = atr * 2
stop_price = latest_price - stop_distance

shares_by_risk = risk_amount / stop_distance
shares_by_capital = max_capital / latest_price

raw_shares = min(shares_by_risk, shares_by_capital)

print(f"Annualized Volatility: {annual_volatility:.2%}")
print(f"Final Shares to Buy: {int(raw_shares)}")