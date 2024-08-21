# Intro

The steps of fator momentum

1. Create a list of all perpetual coins on exchange.
2. Get market data (both past data and live data) for each coin. If a coin has less than a month of data skip it.
3. Calculate VWAP for the live data that is coming in.
4. Define and calculate (using threading) factors based on market data:
    - Size (Market capitalization)
    - Volatility
    - Momentum
5. Construct factor portfolios: for each factor create a long-short portfolio and rebalance this portfolio monthly.
6. Measure factor momentum: look at the monthly performance of each factor portfolio
7. Implement time-series factor momentum: go long factors that have a positive previous month return and short factors that have a negative monthly return. Scale positions based on the factor portfolio performance.
    - Enter any long or short position only with a limit order around the VWAP.
8. Compare to benchmarks: compare the performance of this strategy to holding bitcoin and to holding the spy index.
9. Account for transaction costs and slippage
10. Implement stop-losses and position sizing rules
    - Never let the position of a coin exceed some percentage amount X
11. Rebalance weekly.
12. Save returns of the strategy to an SQL database.
13. Calculate statistics of the strategy including:
    - How much fees have been paid
    - Sharpe ratio before and after fees
    - Residual returns
    - Information ratio
14. 
