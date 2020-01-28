# QuantPortfolio
#BUILD ^DJI PORTFOLIO
    DJI = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO',
           'KO', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ',
           'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG',
           'TRV', 'UNH', 'UTX', 'VZ', 'V', 'WMT', 'WBA', 'DIS',
           '^DJI'
           ]

    SELECTED_YEAR = 2015 # We select data from 2015 January to 2020 January
    DJI_BM_SYM = DJI[-1]
    main(DJI, DJI_BM_SYM, SELECTED_YEAR, risk_free=0.015, start=START, end=END, download=False)
Then we have the following figures
![Cumulative Return](/Portfolio/Figures/%5EDJI/Cumulative_Rets.png)
![Cumulative Return](/Portfolio/Figures/%5EDJI/Efficient_Frontier.png)
![Cumulative Return](/Portfolio/Figures/%5EDJI/Sectoral_Weights_pie.png)
![Cumulative Return](/Portfolio/Figures/%5EDJI/Weights_pie.png)
