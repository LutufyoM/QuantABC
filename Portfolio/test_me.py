'''Run the project'''
import datetime as dt
from pre_run import main

START = dt.datetime(2010, 1, 1)
END = dt.datetime.today()
# ------------Run Program----------------------#
if __name__ == '__main__':
    #BUILD ^DJI PORTFOLIO
    DJI = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO',
           'KO', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ',
           'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG',
           'TRV', 'UNH', 'UTX', 'VZ', 'V', 'WMT', 'WBA', 'DIS',
           '^DJI'
           ]

    SELECTED_YEAR = 2015 # This takes >=
    DJI_BM_SYM = DJI[-1]
    main(DJI, DJI_BM_SYM, SELECTED_YEAR, risk_free=0.015, start=START, end=END, download=False)

    #BUILD ^OMX PORTFOLIO
    OMX = ['TELIA.ST', 'ERIC-B.ST', 'VOLV-B.ST', 'SEB-A.ST',
           'SWED-A.ST', 'SHB-A.ST', 'SAND.ST', 'HM-B.ST',
           'ABB.ST', 'ATCO-A.ST', 'INVE-B.ST', 'ATCO-B.ST', 'STE-R.ST',
           'HEXA-B.ST', 'INDU-C.ST', 'AZN.ST', 'LUND-B.ST', 'STE-A.ST', 'PFE.ST',
           '^OMX']

    OMX_BM_SYM = OMX[-1]
    main(OMX, OMX_BM_SYM, SELECTED_YEAR, risk_free=0.0, start=START, end=END, download=False)
