import yfinance as yf
import pandas as pd
# Example
equity_details = pd.read_csv("C:\\Users\\adity\\Downloads\\EQUITY_L.csv") # All Details for NSE stocks : Symbol is the required field
for name in equity_details.SYMBOL:
    try:
        data = yf.download(f'{name}.NS')
        data.to_csv(f'C:\\Users\\adity\\Desktop\\New Project\\stockdata\\{name}.csv') # Data will be stored in data folder
    except Exception as e:
        print(f'{name} ===> {e}')