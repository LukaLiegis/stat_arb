import yfinance as yf
import pandas as pd

import statsmodels.api as sm

# Get data for WMT and SPY
wmt = yf.download('WMT', start='2021-01-01', end='2021-12-31')
spy = yf.download('SPY', start='2021-01-01', end='2021-12-31')

# Calculate returns
wmt['Return'] = wmt['Close'].pct_change()
spy['Return'] = spy['Close'].pct_change()

# Merge the returns into a single DataFrame
data = pd.merge(wmt['Return'], spy['Return'], left_index=True, right_index=True, suffixes=('_WMT', '_SPY'))

# Perform linear regression
X = sm.add_constant(data['Return_SPY'])
model = sm.OLS(data['Return_WMT'], X)
results = model.fit()

# Get the beta coefficient
beta = results.params['Return_SPY']

print(f'Beta of WMT: {beta}')
import matplotlib.pyplot as plt

# Plot the returns
plt.figure(figsize=(10, 6))
plt.scatter(data['Return_SPY'], data['Return_WMT'], alpha=0.5)
plt.xlabel('SPY Returns')
plt.ylabel('WMT Returns')
plt.title('Scatter Plot of WMT and SPY Returns')

# Plot the linear regression line
plt.plot(data['Return_SPY'], results.fittedvalues, color='red', linewidth=2, label='Linear Regression')

# Add legend
plt.legend()

# Show the plot
plt.show()