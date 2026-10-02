import requests
import numpy as np
import pandas as pd
import yfinance as yf
from io import StringIO

# get S&P 500 tickers
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
response = requests.get(url, headers=headers)

stocks_table = pd.read_html(StringIO(response.text))[0]
tickers = stocks_table['Symbol'].tolist()
tickers = [i.replace('.', '-') for i in tickers]
tickers.append('^GSPC')  # add S&P 500 

# download and calculate returns
data = yf.download(tickers, period="5y", interval="1mo")
prices = data['Close']
returns = prices.pct_change().dropna()


market_returns = returns['^GSPC']
stock_returns = returns.drop(columns=['^GSPC'])

# loop through each stock
results = []

for ticker in stock_returns.columns:
    s_returns = stock_returns[ticker]
    
    combined = pd.concat([s_returns, market_returns], axis=1).dropna()
    
    clean_stock = combined.iloc[:, 0]
    clean_market = combined.iloc[:, 1]
    
    cov = clean_stock.cov(clean_market)
    market_var = clean_market.var()
    
    raw_beta = cov / market_var
    blume_beta = (0.67 * raw_beta) + 0.33
    
    results.append({
        "Ticker": ticker, 
        "Raw Beta": round(raw_beta, 3), 
        "Blume Beta": round(blume_beta, 3)
    })

# build final dataframe
betas = pd.DataFrame(results)

print(betas.head(10))