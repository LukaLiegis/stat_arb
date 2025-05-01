import numpy as np

def calculate_risk_metrics(crypto_dfs, window = 30):

    target_returns = crypto_dfs[0].pct_change()

    realized_vol = target_returns.rolling(window).std() * np.sqrt(365*24*60)
    current_vol = realized_vol.iloc[-1]

    vol_scale = 0.15 / max(0.05, current_vol)

    rolling_max = (1 + target_returns).cumprod().rolling(window).max()
    current_value = (1 + target_returns).cumprod().iloc[-1]
    drawdown = 1 - current_value / rolling_max.iloc[-1]

    drawdown_scale = max(0.5, 1 - drawdown)

    return min(1.0, vol_scale * drawdown_scale)