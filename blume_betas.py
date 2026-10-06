import requests
import numpy as np
import pandas as pd
import yfinance as yf
from io import StringIO

# get data from wikepedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
response = requests.get(url, headers=headers)

stocks_table = pd.read_html(StringIO(response.text))[0]
tickers = stocks_table['Symbol'].tolist()
tickers = [i.replace('.', '-') for i in tickers]
tickers.append('^GSPC')  # add S&P 500 


print("downloading stock data...")
data = yf.download(tickers, period="5y", interval="1mo")
prices = data['Close']
returns = prices.pct_change()

# separate market data from the stock matrix

market_returns = returns['^GSPC']
stock_returns = returns.drop(columns=['^GSPC'])
results = []

# loop through each stock and clean pairs individually
for ticker in stock_returns.columns:
    s_returns = stock_returns[ticker]
    
    combined = pd.concat([s_returns, market_returns], axis=1)
    
    # drop rows where either this stock or the market has missing data
    combined_clean = combined.dropna()

    # makes sure stock has enough history
    
    # if len(combined_clean) < 36:
    #     continue

  
    clean_stock = combined_clean.iloc[:, 0]
    clean_market = combined_clean.iloc[:, 1]
    
    # beta calculation
    cov = clean_stock.cov(clean_market)
    market_var = clean_market.var()
        
    raw_beta = cov / market_var
    blume_beta = (2/3 * raw_beta) + 1/3
    
    results.append({
        "Ticker": ticker, 
        "Raw Beta": round(raw_beta, 3), 
        "Blume Beta": round(blume_beta, 3),
        "Months Used": len(combined_clean)
    })


betas = pd.DataFrame(results)

print("\n--- Top 10 Rows ---")
print(betas.head(10))

betas.to_csv("betas.csv", index=False)