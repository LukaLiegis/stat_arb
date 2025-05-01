import pandas as pd

def calculate_factors(df, lookback_periods=[5, 30, 60, 120, 200]):
    """Calculate momentum and volatility factors"""
    factors = pd.DataFrame(index=df.index)
    returns = df.pct_change()

    for period in lookback_periods:
        factors[f'mom_{period}'] = df.pct_change(period)
        factors[f'vol_{period}'] = returns.rolling(period).std()

        # Higher moment factors
        factors[f'skew_{period}'] = returns.rolling(period).skew()
        factors[f'kurt_{period}'] = returns.rolling(period).kurt()

    return factors.fillna(method='ffill').fillna(method='bfill')