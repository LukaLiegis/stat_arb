import ccxt
import pandas as pd
import os

exchange = ccxt.binance({
    'apiKey': os.environ.get('api_key'),
    'secret': os.environ.get('secret_key'),
    'enableRateLimit': True,
})

def fetch_latest_data(symbols, timeframe = '1m', limit = 1000):
    data = {}
    for symbol in symbols:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit = limit)
            df = pd.DataFrame(ohlcv, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace = True)
            data[symbol] = df['close']
        except Exception as e:
            print(f'Error fetching data for {symbol}: {e}')

    return data
