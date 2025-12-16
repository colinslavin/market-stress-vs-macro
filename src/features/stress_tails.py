from __future__ import annotations
import pandas as pd
import numpy as np
from .stress_utils import log_returns_from_prices


def compute_tail_stress(
    market: pd.DataFrame,
    equity_ticker: str = "SPY",
    window: int = 252,
    q: float = 0.05,
) -> pd.Series:
    """
    Tail-risk / nonlinearity proxy:
    rolling frequency of returns below a rolling quantile threshold.

    No-lookahead rule:
    - the threshold at time t is computed from returns up to t-1 (shifted by 1).

    Output:
    - tail_freq_{window}_{q}: rolling mean of tail events over 'window'
      Higher = more stress.
    """
    close_col = f"close_{equity_ticker.upper()}"
    if close_col not in market.columns:
        raise ValueError(f"market must include {close_col}")

    prices = market[[close_col]].rename(columns={close_col: "equity"})
    r = log_returns_from_prices(prices)["equity"]

    # rolling quantile threshold using past data only
    thresh = r.shift(1).rolling(window).quantile(q)
    is_tail = (r < thresh).astype(float)

    tail_freq = is_tail.rolling(window).mean()
    tail_freq.name = f"tail_freq_{window}_{int(q*100)}"
    return tail_freq
