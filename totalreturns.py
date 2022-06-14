from datetime import datetime
import timepartition
from secrets import IEX_CLOUD_API_TOKEN, IEX_CLOUD_SANDBOX
from iexfinance.stocks import get_historical_data
import requests
from datetime import datetime

## SANDBOX TESTING
import os
os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'

## TOTAL RETURNS INCLUDING DIVIDENDS
def totalReturns(stock, start, end):
    data = get_historical_data(stock, start, end, close_only=True, token=IEX_CLOUD_SANDBOX)
    
    returns = 0
    price_start = data['close'][0]
    price_end = data['close'][-1]
    price_diff = price_end - price_start
    returns += price_diff

    returns = round(returns, 2)

    date_range = timepartition.date_diffRound2(start, end)

    div_amount = 0
    div_url = f"https://sandbox.iexapis.com/stable/stock/{stock}/dividends/{date_range}/?token={IEX_CLOUD_SANDBOX}"
    div_data = requests.get(div_url).json()
    for i in range(len(div_data)):
        try:
            date = div_data[i]['paymentDate']
            date = datetime.strptime(date, '%Y-%m-%d')
            if date >= datetime.strptime(start, '%Y%m%d') and date <= datetime.strptime(end, '%Y%m%d'):
                amount = div_data[i]['amount']
                returns += amount
                div_amount += amount
        except ValueError:
            pass

    div_amount = round(div_amount, 2)

    return [returns, div_amount]

## PRINT STATEMENT
def print_stmnt_returns(stock, start, end):
    result = totalReturns(stock, start, end)
    returns = result[0]
    divs = result[1]
    div_percent = 100*(divs/returns)
    stmnt = f"\n{stock} returned a total of {round(returns, 2)}, including {round(divs, 2)} in dividends, per share.\n{stock} dividends make up {round(div_percent, 2)} percent of total returns.\n"
    return print(stmnt)

## TESTING
if __name__ == '__main__':
    ## EXAMPLE
    os.system('clear')
    start = '20190403'
    end = '20220403'
    stock_list = ['AAPL', 'TSLA', 'MSFT', 'F', 'XOM', 'JPM', 'BRK.B', 'KO']
    for stock in stock_list:
        print_stmnt_returns(stock, start, end)
