"optimize module"
import numpy as np
import pandas as pd
import scipy.optimize as sco

class Initialize:
    "Initialize variables"
    def __init__(self, mean_rets, cov_mat, risk_free):

        self.mean_rets = mean_rets
        self.cov_mat = cov_mat
        self.risk_free = risk_free
        self.efrontier = None

    def performance(self, weights):
        '''
        A function to calculate annualized performance stats
            portfolio return
            portfolio risk (standard deviation)
            portfolio sharpe ratio
        '''
        weights = np.asarray(weights)
        port_ret = np.sum(self.mean_rets * weights)
        port_std = np.sqrt(np.dot(weights.T, np.dot(self.cov_mat, weights)))
        port_sharpe = (port_ret - self.risk_free) / float(port_std)
        return (port_ret, port_std, port_sharpe)

    def port_ret(self, weights):
        "A function to calculate portfolio return"
        return self.performance(weights)[0]

    def port_std(self, weights):
        "A function to calculate portfolio risk"
        return self.performance(weights)[1]

    def neg_sharpe(self, weights):
        "A function to calculate portfolio sharpe ratio"
        return -self.performance(weights)[2]

class Frontier(Initialize):
    "A class for frontier"
    def __init__(self, mean_rets, cov_mat, rf):
        super().__init__(mean_rets, cov_mat, rf)

        self.tickers = list(mean_rets.index)
        self.noa = len(self.tickers)
        self.freq = 252
        self.bounds = ((0, 1),) * self.noa
        self.initial = np.array(self.noa * [1.0 / self.noa])
        self.cons = {"type": "eq", "fun": lambda x: np.sum(x) - 1}

    def update_weights(self, weights):
        "limit weigths"
        weights = weights.copy()
        weights[np.abs(weights) < 1e-5] = 0
        weights = pd.Series(np.round(weights, 5), index=self.tickers)
        return weights

    def global_min_variance(self):
        "A function to calculate the minimum variance portfolio"
        args = ()
        result = sco.minimize(
            self.port_std, args=args, x0=self.initial, method="SLSQP",
            bounds=self.bounds, constraints=self.cons
            )
        weights = result["x"]
        weights = self.update_weights(weights)
        port_ret, port_std, neg_sharpe = self.performance(weights)
        return weights, port_ret, port_std, neg_sharpe

    def max_sharpe_ratio(self):
        "A function to calculate the maximum sharpe ratio portfolio"
        args = ()
        result = sco.minimize(
            self.neg_sharpe, args=args, x0=self.initial, method="SLSQP",
            bounds=self.bounds, constraints=self.cons
            )
        weights = result["x"]
        weights = self.update_weights(weights)
        port_ret, port_std, neg_sharpe = self.performance(weights)
        return weights, port_ret, port_std, neg_sharpe

    def efficint_return(self, target):
        "A function to calculate efficient return portfolio"
        args = ()
        cons = (
            self.cons, {"type": "eq", "fun": lambda x: self.port_ret(x) - target},
                )

        result = sco.minimize(self.port_std, args=args, x0=self.initial,\
                              method="SLSQP", bounds=self.bounds,\
                                  constraints=cons,
                              )
        weights = result["x"]
        weights = self.update_weights(weights)
        port_ret, port_std, neg_sharpe = self.performance(weights)
        return weights, port_ret, port_std, neg_sharpe

    def efficint_frontier(self):
        "A function to create an efficent frontier"
        return self.efrontier
