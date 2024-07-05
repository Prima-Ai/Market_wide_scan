import pandas as pd
import yfinance as yf
import os
import glob

class market_wide_scan:
    def __init__(self):
        self.directory = "C:/MY_PROJECTS/market_wide_scan/data"
        
    def collect_data(self,csv_path):
        csv = pd.read_csv(csv_path)
        symbols = csv['symbol']
        for i in symbols:
            ticker_name = i
            data = yf.download(f"{ticker_name}.NS")
            data.to_csv(f"C:/MY_PROJECTS/market_wide_scan/data/{ticker_name}.csv")
    
    def get_csv_file_paths(self):
        csv_files = glob.glob(os.path.join(self.directory, "*.csv"))
        print("type of csv files", type(csv_files))
        return csv_files

    def get_paras(self, NOD, MA, column_name):
        csv_files = self.get_csv_file_paths()
        for file_path in csv_files:
            data = pd.read_csv(file_path)
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)
            print("length of data is", len(data))
            
            weekly_prices = data['Close'].resample(NOD).last()
            print("length of weekly prices", len(weekly_prices))
            
            data[column_name] = weekly_prices.reindex(data.index, method='ffill')
            weekly_prices_60ma = weekly_prices.rolling(window=MA).mean()
            data['60ma'] = weekly_prices_60ma.reindex(data.index, method='ffill')
            
            fall = []
            for i in range(len(data) - 1):
                fall_of_extent = ((data['60ma'][i + 1] - data['60ma'][i]) / data['60ma'][i]) * 100
                fall.append(fall_of_extent)
            fall.append(0.0)
            
            print("length of fall list", len(fall))
            data['extent_of_fall'] = fall
            
            file_name_with_extension = os.path.basename(file_path)
            file_name, file_extension = os.path.splitext(file_name_with_extension)
            output_path = f"C:/MY_PROJECTS/market_wide_scan/op_files/{file_name}.csv"
            
            data.to_csv(output_path)
            print(f"Saved file: {output_path}")
        
        return "done all process"

path = "C:/MY_PROJECTS/market_wide_scan/data/ADANIENT.csv"
csv = "C:/MY_PROJECTS/market_wide_scan/n200.csv"
scanner = market_wide_scan()
data = scanner.collect_data(csv)
# weekly = scanner.oneweek_scan(path)

# Parameters
NOD = 'W'
MA = 60
column_name = 'Weekly'

# Create an instance of the class and call the method
scanner = market_wide_scan()
paras = scanner.get_paras(NOD, MA, column_name)