import pandas as pd
import numpy as np


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(window=length, min_periods=length).mean()


def ssl_channel(
    df: pd.DataFrame,
    length: int = 10
) -> pd.DataFrame:
    """
    SSL Channel (Ervin Beckers)

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: ['open', 'high', 'low', 'close']
    length : int
        Moving average length

    Returns
    -------
    pd.DataFrame
        Original df with columns:
        - ssl_high
        - ssl_low
        - ssl_dir (1 = bullish, -1 = bearish)
    """

    required_cols = {"open", "high", "low", "close"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"DataFrame must contain {required_cols}")

    df = df.copy()

    # Moving averages
    ma_high = sma(df["high"], length)
    ma_low = sma(df["low"], length)

    ssl_dir = np.zeros(len(df))

    for i in range(len(df)):
        if df["close"].iloc[i] > ma_high.iloc[i]:
            ssl_dir[i] = 1
        elif df["close"].iloc[i] < ma_low.iloc[i]:
            ssl_dir[i] = -1
        else:
            ssl_dir[i] = ssl_dir[i - 1] if i > 0 else 0

    df["ssl_dir"] = ssl_dir
    df["ssl_high"] = np.where(ssl_dir < 0, ma_high, ma_low)
    df["ssl_low"] = np.where(ssl_dir < 0, ma_low, ma_high)

    return df
