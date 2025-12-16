from __future__ import annotations
import pandas as pd
from .stress_utils import log_returns_from_prices


def _panel_close_columns(market: pd.DataFrame) -> list[str]:
    return [c for c in market.columns if c.startswith("close_") and c != "close_^VIX"]


def compute_dispersion_stress(market: pd.DataFrame, window: int = 20) -> pd.Series:
    """
    Disagreement / herding proxy using cross-sectional dispersion.

    Approach:
    - compute daily cross-sectional std of log returns across panel
    - smooth with rolling mean

    Higher = more stress (dislocation/rotation/panic).
    """
    close_cols = _panel_close_columns(market)
    if len(close_cols) < 4:
        raise ValueError("Need several close_* columns to compute dispersion stress.")

    prices = market[close_cols].copy()
    rets = log_returns_from_prices(prices)

    xsec_std = rets.std(axis=1, ddof=0)
    disp = xsec_std.rolling(window).mean()
    disp.name = f"xsec_dispersion_{window}"
    return disp
