import pandas as pd
import yfinance as yf
import os

class MarketWideScan:
    def __init__(self):
        # Use environment variable or default to relative path
        self.data_directory = os.getenv('DATA_DIRECTORY', 'data')
        self.output_directory = os.getenv('OUTPUT_DIRECTORY', 'op_files')
        
        # Ensure directories exist
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(self.output_directory, exist_ok=True)

    def collect_data(self, csv_path):
        csv = pd.read_csv(csv_path)
        symbols = csv['symbol']
        for i in symbols:
            ticker_name = i
            data = yf.download(f"{ticker_name}.NS")
            output_path = os.path.join(self.data_directory, f"{ticker_name}.csv")
            data.to_csv(output_path)
    
    def get_paras(self, path, NOD, MA, column_name):
        data = pd.read_csv(path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        print("length of data is", len(data))
        
        weekly_prices = data['Close'].resample(NOD).last()
        print("length of weekly prices", len(weekly_prices))
        
        data[column_name] = weekly_prices.reindex(data.index, method='ffill')
        # calculate 60ma for weekly data
        weekly_prices_60ma = weekly_prices.rolling(window=MA).mean()
        data['60ma'] = weekly_prices_60ma.reindex(data.index, method='ffill')
        
        fall = []
        for i in range(len(data) - 1):
            fall_of_extent = ((data['60ma'][i + 1] - data['60ma'][i]) / data['60ma'][i]) * 100
            fall.append(fall_of_extent)
        fall.append(0.0)
        print("length of fall list", len(fall))
        
        data['extent_of_fall'] = fall
        output_path = os.path.join(self.output_directory, "Daily.csv")
        data.to_csv(output_path)
        
        return "done all process"


os.environ['DATA_DIRECTORY'] = 'C:/Users/adity/Downloads/Market_wide_scan-market_wide_scan/Market_wide_scan-market_wide_scan/data'
os.environ['OUTPUT_DIRECTORY'] = 'C:/Users/adity/Downloads/Market_wide_scan-market_wide_scan/Market_wide_scan-market_wide_scan/op_files'

# Example usage
csv_path = os.path.join(os.getenv('DATA_DIRECTORY', 'data'), 'n200.csv')
path = os.path.join(os.getenv('DATA_DIRECTORY', 'data'), 'ADANIENT.csv')

scanner = MarketWideScan()
print(scanner.get_paras(path, 'A', 200, 'weekly'))
