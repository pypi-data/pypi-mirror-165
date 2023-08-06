from webbrowser import get
import numpy as np
from . import get_riskless_rate, get_beta, get_risk_premium


def get_capm(ticker, exchange="^gspc") -> float:
    """
    > The CAPM is the riskless rate plus the beta times the risk premium

    @param ticker The ticker of the stock you want to get the CAPM for.
    @param exchange the exchange to use as the market. Default is the S&P 500.

    @return The CAPM is being returned.
    """
    riskless_rate = get_riskless_rate()
    beta = get_beta(ticker, exchange)
    risk_premium = get_risk_premium()
    return np.add(riskless_rate, np.multiply(beta, risk_premium))
