from functools import lru_cache
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from ..histtools import ten_yr_yield_current


@lru_cache(maxsize=5)
def get_corporate_tax_rate(country="United States") -> float:
    """
    It returns the corporate tax rate for a given country

    @param country The country you want to get the corporate tax rate for.

    @return The last value in the Corporate income tax rate column of the dataframe.
    """
    data = pdr.DataReader("CTS_CIT", "oecd")[country]
    return data["Corporate income tax rate"][-1]


@lru_cache(maxsize=5)
def get_market_return() -> float:
    """
    It returns the average of the S&P 500

    @return The average of the S&P 500 returns.
    """
    return np.average(_load_sp500())


def get_riskless_rate() -> float:
    """
    > The riskless rate is the current 10 year US Treasury yield

    @return The current 10 year yield
    """
    return ten_yr_yield_current()


@lru_cache(maxsize=5)
def get_risk_premium() -> float:
    """
    > This function returns the risk premium of the market

    @return The risk premium is the difference between the market return and the riskless rate.
    """
    return np.subtract(get_market_return(), get_riskless_rate())


@lru_cache(maxsize=5)
def _load_sp500() -> pd.DataFrame:
    """
    It loads the S&P 500 historical annual returns data from a CSV file

    @return A dataframe with the S&P 500 historical annual returns.
    """
    return pd.read_csv(
        "valtools/risktools/sp-500-historical-annual-returns.csv"
    ).set_index("date")
