import pandas as pd
from indicators.ssl_channel import ssl_channel

def generate_signals(df: pd.DataFrame, capital: float = 1000, risk_percent: float = 1):
    """
    Generate buy/sell signals based on SSL Channel.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: ['open', 'high', 'low', 'close']
    capital : float
        Total capital in account
    risk_percent : float
        Percent of capital to risk per trade (e.g., 1)

    Returns
    -------
    pd.DataFrame
        df with additional columns:
        - 'signal' : 1 = Buy, -1 = Sell, 0 = Hold
        - 'position_size' : amount to trade
    """

    df = df.copy()
    df = ssl_channel(df, length=10)  # SSL indicator

    # Signal initialization
    signals = []
    position_sizes = []

    position = 0  # 1 = long, -1 = short, 0 = no position

    for i in range(len(df)):
        ssl = df["ssl_dir"].iloc[i]

        # Generate signal
        if ssl == 1 and position != 1:
            signal = 1  # Buy
            position = 1
        elif ssl == -1 and position != -1:
            signal = -1  # Sell
            position = -1
        else:
            signal = 0  # Hold

        # Position size (1% of capital)
        pos_size = capital * (risk_percent / 100) if signal != 0 else 0

        signals.append(signal)
        position_sizes.append(pos_size)

    df["signal"] = signals
    df["position_size"] = position_sizes

    return df
