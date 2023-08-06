from functools import lru_cache
import numpy as np
import pandas as pd
from ..histtools import get_returns


def get_beta(ticker, exchange="^gspc") -> float:
    """
    > We're calculating the covariance of the ticker's returns with the exchange's returns, and dividing
    that by the variance of the ticker's returns

    @param ticker The ticker of the stock you want to get the beta for.
    @param exchange The exchange to use as the market. Default is the S&P 500.

    @return The beta of the stock.
    """
    returns = get_returns(ticker)
    rets_var = returns.var()
    rets_cov = _rets_cov(returns, exchange)
    return np.divide(rets_cov, rets_var)


def _rets_cov(returns, exchange="^gspc") -> float:
    """
    > It takes a `returns` object and an `exchange` string, and returns the covariance between the
    returns of the `returns` object and the returns of the `exchange` string

    @param returns a pandas Series of returns
    @param exchange The exchange to compare the returns to.

    @return The covariance of the returns of the stock and the exchange.
    """
    exchange_rets = _exchange_rets(exchange)
    return returns.cov(exchange_rets)


@lru_cache(maxsize=5)
def _exchange_rets(exchange="^gspc") -> pd.Series:
    """
    > This function returns the returns of the S&P 500 index

    @param exchange The exchange to get the returns for.

    @return A pandas series of the returns of the exchange
    """
    return get_returns(exchange)
