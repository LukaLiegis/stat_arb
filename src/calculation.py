import numpy as np
import pandas as pd
import statsmodels.api as sm
from typing import Tuple


def calculate_stock_beta_idio_volatility(stock_returns: pd.DataFrame, market_returns: pd.DataFrame) -> Tuple[float, float]:
    """
    Calculate the stock's beta and daily idiosyncratic volatility.

    Parameters:
    stock_returns (pd.Series): Series of daily returns for the stock.
    market_returns (pd.Series): Series of daily returns for the market (e.g., S&P 500).

    Returns:
    tuple: (beta, daily_idio_volatility)
    """

    # Ensure the inputs are aligned and drop NaNs
    data = pd.DataFrame({'stock_returns': stock_returns, 'market_returns': market_returns}).dropna()

    # Independent variable (market returns) and adding constant for intercept
    X = sm.add_constant(data['market_returns'])

    # Dependent variable (stock returns)
    Y = data['stock_returns']

    # Perform linear regression to get the beta
    model = sm.OLS(Y, X).fit()
    beta = model.params['market_returns']

    # Calculate the residuals (idiosyncratic returns)
    residuals = model.resid

    # Calculate the daily idiosyncratic volatility
    daily_idio_volatility = np.std(residuals)

    return beta, daily_idio_volatility

def calculate_daily_market_volatility(market_returns: pd.Series) -> float:
    """
    Calculate the daily market volatility.

    Parameters:
    market_returns (pd.Series): Series of daily returns for the market (e.g., S&P 500).

    Returns:
    float: Daily market volatility.
    """
    
    # Calculate the daily market volatility (standard deviation of daily returns)
    daily_market_volatility = np.std(market_returns)
    
    return daily_market_volatility
