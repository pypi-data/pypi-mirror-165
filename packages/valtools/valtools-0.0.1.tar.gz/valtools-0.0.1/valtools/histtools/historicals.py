from functools import lru_cache
import pandas as pd
import yfinance as yf


@lru_cache(maxsize=5)
def get_history(ticker: str, period="max", floaterval="1d") -> pd.DataFrame:
    """
    > This function takes a ticker symbol as a string, and returns a pandas dataframe of the historical
    data for that ticker

    :param ticker: The ticker symbol of the stock you want to get data for
    :type ticker: str
    :param period: str, optional, defaults to max (optional)
    :param floaterval: 1d,5d,1mo,3mo, defaults to 1d (optional)
    :return: A dataframe with the historical data of the ticker
    """
    ticker = yf.Ticker(ticker)
    history = ticker.history(period, floaterval)
    return history


def get_close(ticker: str):
    """
    It takes a ticker symbol as input and returns the closing price of that stock

    :param ticker: The ticker symbol of the stock you want to get the history of
    :type ticker: str
    :return: A pandas series of the closing prices of the stock
    """
    return get_history(ticker)["Close"]
