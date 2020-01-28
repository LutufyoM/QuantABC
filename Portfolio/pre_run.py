'''
This file contain
    1: A class DataFrame with six modules
        a: get_data
        b: cum_growth
        c: daily_log_returns
        d: stock_volatility
        e: covariance
        f: mean_rets
    2: pre_main module and
    3: main module

'''
import os
import numpy as np
import pandas as pd
from download_me import PATH
from download_me import DownloadEngine
from optimize_me import Frontier
import plot_me

class DataFrame:
    "Initialize variables"
    def __init__(self, stocklist, bm_sym):
        self.stocklist = stocklist
        self.bm_sym = bm_sym

    def get_data(self, syms, alldata):
        "Read saved data from csv file"
        path = PATH + alldata
        def sym_to_path(sym, path=path):
            "symbol to path"
            return os.path.join(path, f'{str(sym)}.csv')
        data = pd.DataFrame()
        for sym in syms:
            df_temp = pd.read_csv(sym_to_path(sym), index_col='Date',
                                  parse_dates=True,
                                  usecols=['Date', 'Adj Close'], na_values=['nan'])
            df_temp = df_temp.rename(columns={'Adj Close': sym})
            data = data.join(df_temp, how='outer')
        return data

    def cum_growth(self, data):
        "A function to calculate cumulative growth returns"
        index = data.index[[0]] - (data.index[1]-data.index[0])
        initial = pd.DataFrame(1, columns=data.columns, index=index)
        cum_df = initial.append(data+1).cumprod()- 1
        return cum_df.dot((np.full(cum_df.shape[1], 1.0/cum_df.shape[1])))

    def daily_log_returns(self, data):
        '''A function to calculate daily log returns'''
        log_rets = np.log(1 + data.pct_change().dropna())
        return log_rets

    def stock_volatility(self, data, freq=252):
        '''
        A function to calculate individual stock volatility
           Return annualized standard deviation of every stock.
        '''
        return self.daily_log_returns(data).std() * np.sqrt(freq)

    def covariance(self, data, freq=252):
        '''
        A function to calculate covariance
        Return annualized covariance
        '''
        logret = np.array(self.daily_log_returns(data))[1:]
        logret -= np.mean(logret, axis=0)
        covar = np.dot(logret.T, logret)/(logret.shape[0]-1)
        return covar * freq

    def mean_rets(self, data, freq=252):
        '''
        A function to calculate mean returns
        Return annualized mean returns
        '''
        return self.daily_log_returns(data).mean()* freq

def pre_main(
        df_funct, specific_data, _, bm_sym,
        stocks_rets_included, bm_rets_included, risk_free):
    "pre run"
    mrets = df_funct.mean_rets(specific_data)
    covar = df_funct.covariance(specific_data)

    main_function = Frontier(mrets, covar, risk_free)

    max_weights, _, _, _ = main_function.max_sharpe_ratio()
    max_weights = (max_weights[max_weights > 0])

    min_weights, _, _, _ = main_function.global_min_variance()
    min_weights = (min_weights[min_weights > 0])

    plot_me.display_efficient_frontier(main_function, bm_sym)
    plot_me.display_weights(max_weights, min_weights, bm_sym)
    plot_me.display_sectoral_weights(max_weights, min_weights, bm_sym)

    bm_cum_rets = df_funct.cum_growth(bm_rets_included)
    port_cum_rets = df_funct.cum_growth(stocks_rets_included)
    plot_me.display_cumulative_returns(port_cum_rets, bm_cum_rets, bm_sym)

def main(syms, bm_sym, selected_year, risk_free,
         start, end, download=False):
    "This function call the pre_main function"
    if download:
        download_data = DownloadEngine(start, end)

        #download all stock data
        download_data.stock_data(syms, bm_sym)

        #download info data (sector and industry)
        download_data.get_all_info(syms[:-1], bm_sym)

    #START BUILDING PORTFOLIOS
    stocklist_dir = {
        'stocklist_data':"\\data\\daily_data\\all_{}_stock_lists".format(bm_sym)}

    df_funct = DataFrame(syms[:-1], bm_sym)

    all_data = df_funct.get_data(syms[:-1], stocklist_dir['stocklist_data'])
    selected_alldata = (
        all_data.loc[all_data.index.year >= selected_year])

    bm_data = df_funct.get_data([bm_sym], stocklist_dir['stocklist_data'])
    selected_bmdata = (
        bm_data.loc[bm_data.index.year >= selected_year])

    stocks_returns = df_funct.daily_log_returns(selected_alldata)
    bm_returns = df_funct.daily_log_returns(selected_bmdata)

    pre_main(
        df_funct, selected_alldata, selected_bmdata, bm_sym,
        stocks_returns, bm_returns, risk_free)
if __name__ == "__main__":
    pass
