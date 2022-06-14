# Stock Performance Indicators (SPI)

This repository contains Python modules for analysing the performance of a list of stocks over a specified time range, divided into *periods*.

## Important preliminary information

These modules call data from IEX cloud API, see [here](https://iexcloud.io/). 

In order to run the programs in each module you need to edit the file `secrets.py` and update the values `IEX_ClOUD_SANDBOX` or `IEX_CLOUD_API_TOKEN` with a valid API token from IEX cloud. 

You can make an account and buy tokens on IEX Cloud.

**Note.** *Sandbox environment tokens are free!*

### Environments

Each module in this repository is set to run in the *sandbox environment*. This means the data accessed to measure stock performance is not real world data. Rather, it is a randomized version that loosely approximates real world data. As mentioned above, sandbox environment tokens are freely available from IEX Cloud.

In order to run the modules in this repository on *real world data* you need to: 

- comment out the line `os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'` in the modules `totalreturns.py`, headtohead.py` and `distribution.py`;
- in the `totalReturns` method in the module `totalreturns.py`, replace all instances of `token=IEX_CLOUD_SANDBOX` with `token=IEX_CLOUD_API_TOKEN`;
- in the `headTohead` method in the module `headtohead.py`, replace all instances of `token=IEX_CLOUD_SANDBOX` with `token=IEX_CLOUD_API_TOKEN`;
- in the `distribution` method in the module `distribution.py`, replace all instances of `token=IEX_CLOUD_SANDBOX` with `token=IEX_CLOUD_API_TOKEN`.

## The SPIs

After updating the `secrets.py` module with value(s) for the API tokens, it will be possible to run `main.py`. This is the main module for the stock performance analysers. On running `main.py`, the user is prompted to choose one of three options. The first option runs `totalreturns.py`, the second runs `headtohead.py` and the third runs `distribution.py`.

### Total returns

Option 1 runs `totalreturns.py`. This module calculates, for a list of *US stocks*, a starting date and ending date, the total returns over this time range. For a stock `s`, its total returns over the time period $(t_0, t_1)$ is comprised of: 

- the difference in market price: `s` price at $t_1$ minus `s` price at $t_0$;
- the dividends or distributions paid out per unit of `s` held during $(t_0, t_1)$.

### Head to head

Option 2 runs `headtohead.py`. This module takes in two stocks `s_A`, `s_B`, a time range $(t_0, t_1)$ and an regular period $P$ serving to divide the time range $(t_0, t_1)$ into $P$-many time periods. E.g., if $P = 2$ then $(t_0, t_1)$ is divided into $P=2$ periods: $(t_0, p), (p, t_1)$ where $p$ is a date halfway between $t_0$ and $t_1$. 

The objective of `headtohead.py` is to calculate, with respect to total returns for each stock `s_A`, `s_B` over each time period in the time range, when `s_A` returned more than `s_B` and vice-versa. The module `headtohead.py` returns the percentage of time `s_A` outperformed `s_B` and vice-versa.

### Distribution

Option 3 runs `distribution.py`. The inputs here are similar to option 2, however the module `distribution.py` takes in a list of stocks as in option 1 instead of just two stocks. 

Over a time range and given period `distribution.py` calculates, for a given stock `s` in the list, the percentage of times its performance (with respect to returns) placed it highest among all other stocks in the list, second highest, third highest and so on. 

Accordingly, `distribution.py` returns a simple probability distribution recording the performance of each stock in the stock list relative to others.
