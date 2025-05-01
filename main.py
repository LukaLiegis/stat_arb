import logging
from datetime import time, datetime, timedelta

from src.data import exchange, fetch_latest_data
from src.order_execution import execute_order
from src.position_management import manage_position
from src.prediction import generate_trading_signal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="stat_arb_trading.log",
)

symbols = ['XRPUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
target_symbol = 'XRPUSDT'
target_idx = 0
account_size = 100
model_retrain_interval = 7 * 24 * 60 * 60
position = 0

def wait_until_next_minute():
    now = datetime.now()
    next_minute = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
    wait_seconds = (next_minute - now).total_seconds()

    buffer_seconds = 0.1

    if wait_seconds > 0:
        time.sleep(wait_seconds + buffer_seconds)

    execution_time = datetime.now()
    logging.info(f"Executing at: {execution_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")

def run_trading_bot():
    global position

    last_model_training_time = 0

    while True:
        try:
            wait_until_next_minute()

            current_time = time.time()
            current_datetime = datetime.now()

            logging.info(f"Starting trading cycle at {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

            cycle_start_time = time.time()

            if current_time - last_model_training_time > model_retrain_interval:
                logging.info(f"Retraining model at {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

                history_data = {}
                for symbol in symbols:
                    ohlcv = exchange.fetch_ohlcv()
                    ...

                logging.info(f"Model training done at {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

            logging.info(f"Fetching latest market data at {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            current_data = fetch_latest_data(symbols, timeframe='1m', limit=250)

            prediction = generate_trading_signal(
                [current_data[s.replace('/', '')] for s in symbols],
                target_idx
            )
            logging.info(f"Generated prediction: {prediction:.6f}")

            target_position = manage_position(position, prediction)
            logging.info(f"Current position: {position:.2f}, Target position: {target_position:.2f}")

            # Execute order of position changes
            if target_position != position:
                position = execute_order(target_symbol, target_position, position, account_size)
                logging.info(f"New position: {position:.2f}")

            #TODO: Get account balance and log performance

            # Check if execution took too long
            cycle_duration = time.time() - cycle_start_time
            logging.info(f"Cycle duration: {cycle_duration:.2f}")

            if cycle_duration > 55:
                logging.warning(f"Execution time ({cycle_duration:.2f}s) is approaching the 1-minute limit")

        except Exception as e:
            logging.error(f'Error in main loop: {e}')

if __name__ == '__main__':
    logging.info("Starting trading bot...")
    run_trading_bot()
