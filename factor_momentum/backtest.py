import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pybit.unified_trading import HTTP
import time

class FactorMomentumBacktest:
    def __init__(self, api_key, api_secret, testnet=False, timeframe='1', lookback_period=30, top_n=10):
        self.session = HTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret
        )
        self.timeframe = timeframe  # '1' for monthly in Bybit API
        self.lookback_period = lookback_period
        self.top_n = top_n

    def fetch_all_perpetuals(self):
        response = self.session.get_instruments_info(category="linear")
        return [symbol['symbol'] for symbol in response['result']['list'] if symbol['status'] == 'Trading']

    def fetch_data(self, symbol):
        try:
            end_time = int(time.time() * 1000)
            start_time = end_time - (self.lookback_period * 30 * 24 * 60 * 60 * 1000)  # Approximate 30 days per month
            response = self.session.get_kline(
                category="linear",
                symbol=symbol,
                interval=self.timeframe,
                start=start_time,
                end=end_time,
                limit=self.lookback_period
            )
            df = pd.DataFrame(response['result']['list'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df['symbol'] = symbol
            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def calculate_monthly_returns(self, df):
        df['monthly_return'] = df['close'].astype(float).pct_change()
        return df

    def run_backtest(self, start_date, end_date):
        all_perpetuals = self.fetch_all_perpetuals()
        all_data = []

        for symbol in all_perpetuals:
            df = self.fetch_data(symbol)
            if df is not None and not df.empty:
                df = self.calculate_monthly_returns(df)
                all_data.append(df)

        combined_data = pd.concat(all_data)
        combined_data = combined_data[(combined_data.index >= start_date) & (combined_data.index <= end_date)]

        results = []
        for date in combined_data.index.unique():
            monthly_data = combined_data[combined_data.index == date]
            sorted_returns = monthly_data.sort_values('monthly_return', ascending=False)
            
            long_positions = sorted_returns.head(self.top_n)['symbol'].tolist()
            short_positions = sorted_returns.tail(self.top_n)['symbol'].tolist()
            
            results.append({
                'date': date,
                'long_positions': long_positions,
                'short_positions': short_positions
            })

        return pd.DataFrame(results)

    def calculate_portfolio_performance(self, backtest_results):
        portfolio_returns = []

        for i in range(1, len(backtest_results)):
            prev_month = backtest_results.iloc[i-1]
            curr_month = backtest_results.iloc[i]
            
            long_returns = curr_month[curr_month['symbol'].isin(prev_month['long_positions'])]['monthly_return']
            short_returns = curr_month[curr_month['symbol'].isin(prev_month['short_positions'])]['monthly_return']
            
            portfolio_return = (long_returns.mean() - short_returns.mean()) / 2  # Equal weight to long and short
            portfolio_returns.append(portfolio_return)

        return pd.Series(portfolio_returns)

def main():
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    testnet = False  # Set to True if you want to use the testnet

    backtest = FactorMomentumBacktest(api_key, api_secret, testnet)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    results = backtest.run_backtest(start_date, end_date)
    print(results)

    portfolio_performance = backtest.calculate_portfolio_performance(results)
    cumulative_returns = (1 + portfolio_performance).cumprod()
    
    print(f"Cumulative Return: {cumulative_returns.iloc[-1]}")
    print(f"Annualized Return: {(cumulative_returns.iloc[-1] ** (12/len(cumulative_returns)) - 1) * 100:.2f}%")

if __name__ == "__main__":
    main()