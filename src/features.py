import pandas as pd
from factors import calculate_factors

def prepare_features(crypto_dfs, target_crypto_idx=0):
    """Prepare features for prediction"""
    all_factors = []

    for i, df in enumerate(crypto_dfs):
        factors = calculate_factors(df)
        factors = factors.add_suffix(f'_crypto_{i}')
        all_factors.append(factors)

    X = pd.concat(all_factors, axis=1)
    y = crypto_dfs[target_crypto_idx].pct_change().shift(-1)

    valid_idx = ~(X.isna().any(axis=1) | y.isna())
    X = X[valid_idx]
    y = y[valid_idx]

    return X, y