import pandas as pd
from . import get_close


def get_returns(ticker: str) -> pd.Series:
    """
    It takes a ticker symbol as input, and returns the daily returns of that ticker

    @param ticker The ticker symbol of the stock you want to get data for.

    @return A series of the percent change of the closing price of the ticker.
    """
    return get_close(ticker).pct_change().dropna()
