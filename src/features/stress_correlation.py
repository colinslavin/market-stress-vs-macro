from __future__ import annotations
import pandas as pd
from .stress_utils import log_returns_from_prices


def _panel_close_columns(market: pd.DataFrame) -> list[str]:
    return [c for c in market.columns if c.startswith("close_") and c != "close_^VIX"]


def compute_correlation_stress(market: pd.DataFrame, window: int = 60) -> pd.Series:
    """
    Diversification breakdown proxy:
    rolling average pairwise correlation across a sector ETF panel.

    Higher = more stress (correlations converge toward 1 in crises).
    """
    close_cols = _panel_close_columns(market)
    if len(close_cols) < 4:
        raise ValueError("Need several close_* columns to compute correlation stress.")

    prices = market[close_cols].copy()
    rets = log_returns_from_prices(prices).dropna(how="any")

    # Rolling average pairwise correlation
    # For each date, compute corr matrix over window and average off-diagonals.
    vals = []
    idx = []
    for i in range(window, len(rets) + 1):
        w = rets.iloc[i - window:i]
        corr = w.corr()
        # average off-diagonal
        n = corr.shape[0]
        off_diag_mean = (corr.values.sum() - n) / (n * (n - 1))
        vals.append(off_diag_mean)
        idx.append(rets.index[i - 1])

    return pd.Series(vals, index=pd.to_datetime(idx), name=f"avg_pairwise_corr_{window}")
