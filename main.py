from src.calculation import calculate_stock_beta_idio_volatility, calculate_daily_market_volatility
import yfinance as yf

market_data = yf.download("SPY", start="2018-01-01", end="2019-01-01")
wmt = yf.download("WMT", start="2018-01-01", end="2019-01-01")
syf = yf.download("SYF", start="2018-01-01", end="2019-01-01")

# Calculate daily returns
wmt_returns = wmt['Adj Close'].pct_change().dropna()
syf_returns = syf['Adj Close'].pct_change().dropna()
market_returns = market_data['Adj Close'].pct_change().dropna()

beta_wmt, idio_volatility_wmt = calculate_stock_beta_idio_volatility(wmt_returns, market_returns)
beta_syf, idio_volatility_syf = calculate_stock_beta_idio_volatility(syf_returns, market_returns)
market_volatility = calculate_daily_market_volatility(market_returns)

nmv_wmt = 10_000_000
nvm_syf = 5_000_000
nvm_spy = 10_000_000

print("\nResults of WMT:")
print(f"Beta of WMT: {beta_wmt}")
print(f"Idiosyncratic volatility of WMT: {idio_volatility_wmt}")
print("\nResults of SYF:")
print(f"Beta of SYF: {beta_syf}")
print(f"Idiosyncratic volatility of SYF: {idio_volatility_syf}")
print(f"\nMarket volatility: {market_volatility}")

portfolio_beta = beta_wmt * nmv_wmt + beta_syf * nvm_syf + 1 * nvm_spy
print(f"\nPortfolio beta: {portfolio_beta}")

portfolio_market_vol = portfolio_beta * market_volatility
print(f"\nPortfolio market volatility: {portfolio_market_vol.round(2)}")