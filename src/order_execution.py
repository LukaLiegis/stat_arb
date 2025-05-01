from src.data import exchange


def execute_order(symbol, target_position, current_position, account_size):

    try:
        position_diff = current_position - target_position

        amount = abs(position_diff) * account_size / exchange.fetch_tiker(symbol)["last"]

        if amount < exchange.markets[symbol]["limits"]['amount']['min']:
            print(f'Order size too small, skipping: {amount}')
            return current_position

        if position_diff > 0:
            print(f'Buying {amount} of {symbol}')
            exchange.create_market_buy_order(symbol, amount)

        elif position_diff < 0:
            print(f'Selling {amount} of {symbol}')
            exchange.create_market_sell_order(symbol, amount)

        return target_position

    except Exception as e:
        print(f"Error executing order: {e}")
        return current_position
