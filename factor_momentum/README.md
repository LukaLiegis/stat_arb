# Intro

The steps of fator momentum

1. Create a list of all perpetual coins on exchange.
2. Get market data for each coin. If a coin has less than a month of data skip it.
3. Define and calculate (using threading) factors based on market data:
    - Size (Market capitalization)
    - Volatility
    - Momentum
4. Construct factor portfolios: for each factor create a long-short portfolio and rebalance this portfolio monthly.
5. Measure factor momentum: look at the monthly performance of each factor portfolio
6. Implement time-series factor momentum: go long factors that have a positive previous month return and short factors that have a negative monthly return. Scale positions based on the factor portfolio performance.
7. Compare to benchmarks: compare the performance of this strategy to holding bitcoin and to holding the spy index.
8. Account for transaction costs and slippage
9. Implement stop-losses and position sizing rules
10. Rebalance weekly.
