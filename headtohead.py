import timepartition
from collections import defaultdict
from iexfinance.stocks import get_historical_data
from secrets import IEX_CLOUD_API_TOKEN, IEX_CLOUD_SANDBOX
import requests
from datetime import datetime
from datetime import timedelta

## SANDBOX TESTING
import os
os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'

## IF NO DATA AT SPECIFIED DATE, GO TO NEXT DAY
def priceDateVerifyAdd(stockPrice_data, date):
    try:
        return stockPrice_data['close'][date]
    except KeyError:
        date = datetime.strptime(date, '%Y%m%d')
        date = date + timedelta(days=1)
        date = date.strftime('%Y%m%d')
        return priceDateVerifyAdd(stockPrice_data, date)

## IF NO DATA AT SPECIFIED DATE, GO TO PREVIOUS DAY
def priceDateVerifySub(stockPrice_data, date):
    try:
        return stockPrice_data['close'][date]
    except KeyError:
        date = datetime.strptime(date, '%Y%m%d')
        date = date - timedelta(days=1)
        date = date.strftime('%Y%m%d')
        return priceDateVerifySub(stockPrice_data, date) 

## MAIN PROGRAM FOR HEAD TO HEAD ANALYSIS
def headTohead(stock_A, stock_B, start, end, intv):
    dates = timepartition.date_range(start, end, intv)
    dates = list(dates)

    date_range = timepartition.date_diffRound2(start, end)

    performance = defaultdict(int)

    priceData_A = get_historical_data(stock_A, start, end, close_only=True, token=IEX_CLOUD_SANDBOX)
    divData_A_url = f"https://sandbox.iexapis.com/stable/stock/{stock_A}/dividends/{date_range}/?token={IEX_CLOUD_SANDBOX}"
    divData_A = requests.get(divData_A_url).json()

    priceData_B = get_historical_data(stock_B, start, end, close_only=True, token=IEX_CLOUD_SANDBOX)
    divData_B_url = f"https://sandbox.iexapis.com/stable/stock/{stock_B}/dividends/{date_range}/?token={IEX_CLOUD_SANDBOX}"
    divData_B = requests.get(divData_B_url).json()

    for i, d in enumerate(dates):
        returns_A_i = 0
        returns_B_i = 0

        if i < len(dates) - 1:
            start_i = d
            end_i = dates[i+1]

            start_price_A_i = priceDateVerifyAdd(priceData_A, start_i)
            end_price_A_i = priceDateVerifySub(priceData_A, end_i)
            diff = end_price_A_i - start_price_A_i
            returns_A_i += diff

            for div in divData_A:
                try:
                    div_date = div['paymentDate']
                    div_date = datetime.strptime(div_date, '%Y-%m-%d')
                    if div_date >= datetime.strptime(start_i, '%Y%m%d') and div_date <= datetime.strptime(end_i, '%Y%m%d'):
                        returns_A_i += div['amount']
                except ValueError:
                    pass
            
            start_price_B_i = priceDateVerifyAdd(priceData_B, start_i)
            end_price_B_i = priceDateVerifySub(priceData_B, end_i)
            diff = end_price_B_i - start_price_B_i
            returns_B_i += diff

            for div in divData_B:
                try:
                    div_date = div['paymentDate']
                    div_date = datetime.strptime(div_date, '%Y-%m-%d')
                    if div_date >= datetime.strptime(start_i, '%Y%m%d') and div_date <= datetime.strptime(end_i, '%Y%m%d'):
                        returns_B_i += div['amount']
                except ValueError:
                    pass
            
            if returns_A_i > returns_B_i:
                performance[stock_A] += 1
            if returns_A_i < returns_B_i:
                performance[stock_B] += 1
            if returns_A_i == returns_B_i:
                performance[stock_A] += 0.5
                performance[stock_B] += 0.5
    
    return performance

## PRINTS RESULTS OF headTohead
def print_stmnt_performance(stock_A, stock_B, start, end, intv):
    perf_dict = headTohead(stock_A, stock_B, start, end, intv)
    total = intv

    chance = {
        stock_A: f"{round(100*perf_dict[stock_A]/total, 2)} percent",
        stock_B: f"{round(100*perf_dict[stock_B]/total, 2)} percent"
    }

    print(f"Over {intv} regular periods:")
    for key in chance:
        print(f"{key} outperformed {chance[key]} of the time.")

    return

## TESTING
if __name__ == '__main__':
    start = '20180622'
    end = '20210403'

    stock_A = 'AAPL'
    stock_B = 'MSFT'

    intv = 150
    print(headTohead(stock_A, stock_B, start, end, intv))
    print_stmnt_performance(stock_A, stock_B, start, end, intv)
