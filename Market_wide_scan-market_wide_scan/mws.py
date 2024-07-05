import pandas as pd
import yfinance as yf

class market_wide_scan:
    def collect_data(self,csv_path):
        csv = pd.read_csv(csv_path)
        symbols = csv['symbol']
        for i in symbols:
            ticker_name = i
            data = yf.download(f"{ticker_name}.NS")
            data.to_csv(f"C:\\Users\\adity\\Downloads\\Market_wide_scan-market_wide_scan\\Market_wide_scan-market_wide_scan\\data\\{ticker_name}.csv")
    
    def get_paras(self,path,NOD,MA,column_name):
        data = pd.read_csv(path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date',inplace=True)
        print("length of data is",len(data))
        weekly_prices = data['Close'].resample(NOD).last()
        print("lenght of weekly prices",len(weekly_prices))
        data[column_name] = weekly_prices.reindex(data.index,method='ffill')
        # calculate 60ma for weekly data
        weekly_prices_60ma = weekly_prices.rolling(window=MA).mean()
        data['60ma'] = weekly_prices_60ma.reindex(data.index, method='ffill')
        fall = []
        for i in range(len(data)-1):
            fall_of_extent = ((data['60ma'][i+1] - data['60ma'][i])/data['60ma'][i])*100
            fall.append(fall_of_extent)
        fall.append(0.0)
        print("lenght of fall list",len(fall))
        data['extent_of_fall'] = fall
        data = data.to_csv("Market_wide_scan-market_wide_scan//op_files//Daily.csv")
        return "done all process"

path = "C:\\Users\\adity\\Downloads\\Market_wide_scan-market_wide_scan\\Market_wide_scan-market_wide_scan\\data\\ADANIENT.csv"
csv = "C:\\Users\\adity\Downloads\Market_wide_scan-market_wide_scan\\Market_wide_scan-market_wide_scan\\n200.csv"
scanner = market_wide_scan()


# Test Case 5: Annual resampling, 200-day moving average
print(scanner.get_paras(path, 'A', 200, 'weekly'))


