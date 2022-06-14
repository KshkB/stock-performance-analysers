from datetime import date
from importlib_metadata import distribution
import timepartition
from collections import defaultdict
from iexfinance.stocks import get_historical_data
from secrets import IEX_CLOUD_API_TOKEN, IEX_CLOUD_SANDBOX
import requests
from headtohead import priceDateVerifyAdd, priceDateVerifySub
from datetime import datetime
import operator

import pandas as pd

## SANDBOX TESTING
import os
os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'

def distribution(stock_list, start, end, intv):
    dates = timepartition.date_range(start, end, intv)
    dates = list(dates)

    date_range = timepartition.date_diffRound2(start, end)

    perf_dist = {stock: defaultdict(int) for stock in stock_list}

    data_set = {}
    for stock in stock_list:
        data_set[f"{stock} data"] = get_historical_data(stock, start, end, close_only=True, token=IEX_CLOUD_SANDBOX)
        dividends_url = f"https://sandbox.iexapis.com/stable/stock/{stock}/dividends/{date_range}/?token={IEX_CLOUD_SANDBOX}"
        dividends = requests.get(dividends_url).json()
        data_set[f"{stock} dividends"] = dividends 

    for i, d in enumerate(dates):
        if i < len(dates)-1:
            start_i = d
            end_i = dates[i+1]
            
            returns_result = []

            for stock in stock_list:
                stock_returns = 0

                stock_data = data_set[f"{stock} data"]
                startPrice = priceDateVerifyAdd(stock_data, start_i)
                endPrice = priceDateVerifySub(stock_data, end_i)
                diff = endPrice - startPrice
                stock_returns+= diff

                stock_divs = data_set[f"{stock} dividends"]
                for div in stock_divs:
                    try:
                        div_date = div['paymentDate']
                        div_date = datetime.strptime(div_date, '%Y-%m-%d')
                        if div_date >= datetime.strptime(start_i, '%Y%m%d') and div_date <= datetime.strptime(end_i, '%Y%m%d'):
                            stock_returns += div['amount']
                    except ValueError:
                        pass
                
                returns_result.append([stock, stock_returns])
            
            returns_result.sort(key=operator.itemgetter(1))
            for i, v in enumerate(returns_result):
                stock = v[0]
                perf_dist[stock][i] += 1
     
    return perf_dist      

def print_stmnt(stock_list, start, end, intv):
    perf_dist = distribution(stock_list, start, end, intv)
    

    df_columns = [f"Position {i+1}" for i in range(len(stock_list))]
    results_table = pd.DataFrame(columns = df_columns)
    results_table.insert(loc=0, column='Ticker', value=[])
    for stock in perf_dist:
        row = [stock]
        for i in range(len(stock_list)):
            percentage = round(100*perf_dist[stock][i]/intv, 2)
            row.append(percentage)

        results_table = results_table.append(
            pd.Series(
                row, index = results_table.columns
            ),ignore_index=True
        )

    
    return results_table.to_string(index=False)

## TESTING
if __name__ == '__main__':
    start = '20100622'
    end = '20210403'

    stock_list = [
        'AAPL', 'MSFT', 'KO', 'JPM', 'SPY', 'BRK.B'
    ]

    intv = 200

    print(print_stmnt(stock_list, start, end, intv))

