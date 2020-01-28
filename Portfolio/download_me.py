'''
Class Download Engine contain two module:
    1: A module to download daily ticker data and
    2: A module to download sector anf industry info.
'''
import os
import pandas_datareader.data as web
import pandas as pd
import requests
from requests.exceptions import HTTPError

PATH = os.path.dirname(os.path.realpath(__file__))

class DownloadEngine:
    "Initialize variables"
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.key_info_path = '\\data\\company_info'

    def stock_data(self, syms, bm_sym):
        "A function to download daily stock data and save to csv file"
        _ = '\\data\\daily_data\\all_{}_stock_lists'.format(bm_sym)

        if not os.path.exists(PATH + _):
            os.makedirs(PATH + _)
        for sym in syms:
            try:
                print('Fetching %s.....' % sym)
                data = web.DataReader(sym, 'yahoo', self.start, self.end)
            except IndexError:
                print('Element not found for:'+ sym)
            data.to_csv(os.path.join(PATH + _, '%s.csv' % sym))
        print(
            'All {} stocks data has successfully been'.format(len(syms)) +
            'saved in the folder located at {}'.format(PATH + _))
        print()

    def get_all_info(self, syms, bm_sym):
        "A function to  download Sector & Industry info for every ticker & save to csv file"
        if not os.path.exists(PATH + self.key_info_path):
            os.makedirs(PATH + self.key_info_path)
        count = 0

        columns = ['Sector', 'Industry']
        info_df = pd.DataFrame(columns=columns, index=syms)
        for sym in syms:

            #1: Sector and Industry info:
            sym = sym.replace('_', '/')
            url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'\
                + '%s?lang=en-US&region=US&modules=assetProfile&corsDomain=finance.yahoo.com'% (sym)
            try:
                req = requests.get(url)
                req.raise_for_status()
                req = req.json()
            except HTTPError:
                print('Nothing downloaded')
            else:
                html = req
            try:
                sector = html['quoteSummary']['result'][0]['assetProfile']['sector']
                info_df.at[syms[count], "Sector"] = sector
            except IndexError:
                print('Nothing found for:'+sym)
            try:
                industry = html['quoteSummary']['result'][0]['assetProfile']['industry']
                info_df.at[syms[count], "Industry"] = industry
            except IndexError:
                print('Nothing found for:' + sym)

            count += 1
        info_df.index.names = ['Symbol']
        info_df.to_csv(PATH + self.key_info_path
                       + '\\{}_comp_info.csv'.format(bm_sym), index=True)
        print(
            'Company_info for {} stock lists has successfully'.format(bm_sym)+
            'been saved in the folder located at {}'.format(
                PATH + self.key_info_path))
        print()

if __name__ == '__main__':
    pass
