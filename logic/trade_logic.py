import pandas as pd
import numpy as np

def calculate_g_channel(df, length=100):
    """Calculate G-Channel indicators."""
    df['a'] = np.nan
    df['b'] = np.nan
    df['a'] = df['close'].rolling(window=length, min_periods=1).max()
    df['b'] = df['close'].rolling(window=length, min_periods=1).min()
    df['avg'] = (df['a'] + df['b']) / 2

    # Determine buy and sell signals
    df['crossup'] = (df['b'].shift(1) < df['close'].shift(1)) & (df['b'] > df['close'])
    df['crossdn'] = (df['a'].shift(1) < df['close'].shift(1)) & (df['a'] > df['close'])
    df['bullish'] = df['crossup'] & ~df['crossdn']
    df['bearish'] = df['crossdn'] & ~df['crossup']

    return df

def calculate_ema(df, lengths=[13, 25, 55]):
    """Calculate EMAs for given lengths."""
    for length in lengths:
        df[f'ema_{length}'] = df['close'].ewm(span=length, adjust=False).mean()
    return df

def apply_trading_strategy(df):
    """Apply the trading strategy based on G-Channel and EMA."""
    # Buy when G-Channel gives a buy signal and price is below EMA
    df['buy_signal'] = df['bullish'] & (df['close'] < df['ema_55'])

    # Sell when G-Channel gives a sell signal and price is above EMA
    df['sell_signal'] = df['bearish'] & (df['close'] > df['ema_55'])

    return df

# Example usage
# Assuming `data` is a DataFrame with a 'close' column containing historical price data
data = pd.DataFrame({
    'close': [100, 102, 101, 105, 107, 110, 108, 107, 109, 111, 115, 113, 112, 114, 116]
})

# Calculate indicators
data = calculate_g_channel(data)
data = calculate_ema(data)

# Apply trading strategy
data = apply_trading_strategy(data)

# Display results
print(data[['close', 'avg', 'ema_55', 'buy_signal', 'sell_signal']])