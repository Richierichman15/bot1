import pandas as pd
import numpy as np
import requests

from logic.trade_logic import calculate_g_channel, calculate_ema, apply_trading_strategy

def fetch_historical_data(coin_id, vs_currency='usd', days=30):
    """Fetch historical market data from CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={days}"
    response = requests.get(url)
    data = response.json()
    
    # Extract prices and convert to DataFrame
    prices = data['prices']  # List of [timestamp, price]
    df = pd.DataFrame(prices, columns=['timestamp', 'close'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime
    df.set_index('timestamp', inplace=True)  # Set timestamp as index
    return df

def simulate_trading(df):
    """Simulate trading based on buy/sell signals."""
    initial_balance = 10000  # Starting balance
    balance = initial_balance
    position = 0  # Number of shares/units held
    for index, row in df.iterrows():
        if row['buy_signal'] and balance > 0:  # Buy signal
            position = balance / row['close']  # Buy as much as possible
            balance = 0  # All balance used for buying
            print(f"Buying at {row['close']} on {index}")
        elif row['sell_signal'] and position > 0:  # Sell signal
            balance = position * row['close']  # Sell all
            position = 0  # No position held
            print(f"Selling at {row['close']} on {index}")

    # Final balance calculation
    final_balance = balance + (position * df.iloc[-1]['close'])  # Add any remaining position value
    return final_balance

# Example usage with historical data from CoinGecko
coin_id = 'bitcoin'  # Replace with the desired coin ID
data = fetch_historical_data(coin_id, vs_currency='usd', days=30)

# Calculate indicators
data = calculate_g_channel(data)
data = calculate_ema(data)

# Apply trading strategy
data = apply_trading_strategy(data)

# Simulate trading
final_balance = simulate_trading(data)
print(f"Final balance: {final_balance}")
