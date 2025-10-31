# src/fetch_data.py
import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

def fetch_prices(symbols, start, end, save_path='data'):
    os.makedirs(save_path, exist_ok=True)
    all_data = pd.DataFrame()

    for s in symbols:
        df = yf.download(s, start=start, end=end, progress=False)['Close']
        df.name = s
        all_data[s] = df

    all_data = all_data.dropna()
    file_path = os.path.join(save_path, 'crypto_prices.csv')
    all_data.to_csv(file_path)
    print(f"Data saved to {file_path}")
    return all_data

if __name__ == "__main__":
    symbols = ["BTC-USD", "ETH-USD", "LTC-USD", "MATIC-USD", "AVAX-USD"]
    
    # Use longer period: last 3 years
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=3*365)).strftime('%Y-%m-%d')
    
    fetch_prices(symbols, start_date, end_date)
