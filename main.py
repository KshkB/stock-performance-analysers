import totalreturns
import headtohead
import distribution
import os

if __name__ == '__main__':
    os.system('clear')
    print('What would you like to do?')
    print('1. Find the total returns (including dividends) for a stock or list of stocks;')
    print('2. Compare the performance of one stock against another;')
    print('3. Get the performance distribution for a list of stocks.')
    user_input = int(input().strip())
    os.system('clear')

    if user_input == 1:
        print('How many stocks are in your list?')
        user_input2 = int(input().strip())
        os.system('clear')

        stock_list = []
        for i in range(user_input2):
            print(f'Enter the ticker of stock number {i+1}')
            stock = str(input().strip())
            stock_list.append(stock)
    
        os.system('clear')
        print('Enter the starting and ending dates to inspect:')
        print('Starting year:')
        start_yr = str(input().strip())
        print('Starting month:')
        start_mth = str(input().strip())
        if len(start_mth) == 1:
            start_mth = '0'+start_mth
        print('Starting day:')
        start_day = str(input().strip())
        if len(start_day) == 1:
            start_day = '0'+start_day

        start = start_yr+start_mth+start_day

        print('Ending year:')
        end_yr = str(input().strip())
        print('Ending month:')
        end_mth = str(input().strip())
        if len(end_mth) == 1:
            end_mth = '0'+end_mth
        print('Ending day:')
        end_day = str(input().strip())
        if len(end_day) == 1:
            end_day = '0'+end_day

        end = end_yr + end_mth + end_day

        os.system('clear')
        for stock in stock_list:
            totalreturns.print_stmnt_returns(stock, start, end)

    if user_input == 2:
        os.system('clear')
        print('Enter the ticker of stocks to compare.')
        print('First stock:')
        stock_A = str(input().strip())
        print('Second stock:')
        stock_B = str(input().strip())

        os.system('clear')
        print('Enter the starting date to inspect:')
        print('Starting year:')
        start_yr = str(input().strip())
        print('Starting month:')
        start_mth = str(input().strip())
        if len(start_mth) == 1:
            start_mth = '0'+start_mth
        print('Starting day:')
        start_day = str(input().strip())
        if len(start_day) == 1:
            start_day = '0'+start_day

        start = start_yr+start_mth+start_day

        print('Ending year:')
        end_yr = str(input().strip())
        print('Ending month:')
        end_mth = str(input().strip())
        if len(end_mth) == 1:
            end_mth = '0'+end_mth
        print('Ending day:')
        end_day = str(input().strip())
        if len(end_day) == 1:
            end_day = '0'+end_day

        end = end_yr + end_mth + end_day

        os.system('clear')
        print('Enter the number of time periods over which to compare:')
        intv = int(input().strip())
        os.system('clear')
        headtohead.print_stmnt_performance(stock_A, stock_B, start, end, intv)

    if user_input == 3:
        print('How many stocks are in your list?')
        user_input2 = int(input().strip())
        os.system('clear')

        stock_list = []
        for i in range(user_input2):
            print(f'Enter the ticker of stock number {i+1}')
            stock = str(input().strip())
            stock_list.append(stock)

        os.system('clear')
        print('Enter the starting and ending dates to inspect:')
        print('Starting year:')
        start_yr = str(input().strip())
        print('Starting month:')
        start_mth = str(input().strip())
        if len(start_mth) == 1:
            start_mth = '0'+start_mth
        print('Starting day:')
        start_day = str(input().strip())
        if len(start_day) == 1:
            start_day = '0'+start_day

        start = start_yr+start_mth+start_day

        print('Ending year:')
        end_yr = str(input().strip())
        print('Ending month:')
        end_mth = str(input().strip())
        if len(end_mth) == 1:
            end_mth = '0'+end_mth
        print('Ending day:')
        end_day = str(input().strip())
        if len(end_day) == 1:
            end_day = '0'+end_day

        end = end_yr + end_mth + end_day

        os.system('clear')
        print('Enter the number of time periods over which to inspect:')
        intv = int(input().strip())
        os.system('clear')
        print(distribution.print_stmnt(stock_list, start, end, intv))
