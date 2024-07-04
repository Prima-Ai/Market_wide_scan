import pandas as pd
import yfinance as yf

class market_wide_scan:
    def collect_data(self,csv_path):
        csv = pd.read_csv(csv_path)
        symbols = csv['symbol']
        for i in symbols:
            ticker_name = i
            data = yf.download(f"{ticker_name}.NS")
            data.to_csv(f"C:/MY_PROJECTS/market_wide_scan/data/{ticker_name}.csv")
    
    def oneweek_scan(self,path):
        data = pd.read_csv(path, parse_dates=['Date'])
        data.set_index('Date',inplace=True)
        print("the lenght of data is",len(data))
        
        # calculate weekly prices
        weekly_prices = data['Close'].resample('W').last()
        print("lenght of weekly prices",len(weekly_prices))
        data['weekly'] = weekly_prices.reindex(data.index, method='ffill')
        
        # calculate 60ma for weekly prices
        weekly_prices_60ma = weekly_prices.rolling(window=60).mean()
        data['60_weekly_ma'] = weekly_prices_60ma.reindex(data.index, method='ffill')
        data_till60ma = data.to_csv("C:/MY_PROJECTS/market_wide_scan/op_files/ADANIENT.csv")
        return "script ran sucessfully"


path = "C:/MY_PROJECTS/market_wide_scan/data/ADANIENT.csv"
csv = "C:/MY_PROJECTS/market_wide_scan/n200.csv"
scanner = market_wide_scan()
data = scanner.collect_data(csv)
# weekly = scanner.oneweek_scan(path)