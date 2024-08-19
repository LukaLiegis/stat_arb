import yfinance as yf
import pandas as pd
import statsmodels.api as sm

def calculate_beta(stock_ticker, start_date, end_date):
    # Get data for the stock and the market
    stock = yf.download(stock_ticker, start=start_date, end=end_date)
    market = yf.download("SPY", start=start_date, end=end_date)

    # Calculate returns
    stock['Return'] = stock['Close'].pct_change()
    market['Return'] = market['Close'].pct_change()

    # Drop NaN values
    stock = stock.dropna(subset=['Return'])
    market = market.dropna(subset=['Return'])

    # Merge the returns into a single DataFrame
    data = pd.merge(stock['Return'], market['Return'], left_index=True, right_index=True, suffixes=('_stock', '_market'))

    # Perform linear regression
    X = sm.add_constant(data['Return_market'])
    model = sm.OLS(data['Return_stock'], X)
    results = model.fit()

    # Get the beta coefficient
    beta = results.params['Return_market']

    return beta