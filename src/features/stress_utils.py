from __future__ import annotations
import numpy as np
import pandas as pd


def log_returns_from_prices(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute log returns from price columns.
    Assumes strictly positive prices.
    """
    return np.log(price_df).diff()


def rolling_zscore(x: pd.Series, window: int) -> pd.Series:
    """
    Rolling z-score using past window (includes current x_t in window).
    This is okay for monitoring; for strict no-peek variants, shift before rolling.
    """
    mu = x.rolling(window).mean()
    sd = x.rolling(window).std(ddof=0)
    return (x - mu) / sd
