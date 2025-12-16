from __future__ import annotations
import numpy as np
import pandas as pd
from .stress_utils import log_returns_from_prices


def compute_volatility_indicators(market: pd.DataFrame, equity_ticker: str = "SPY") -> pd.DataFrame:
    """
    Volatility / uncertainty repricing indicators.

    Outputs:
    - vix_level: VIX close
    - vix_log_change: log(VIX_t / VIX_{t-1})
    - rv_20: 20d realized vol (annualized) of SPY log returns
    - rv_60: 60d realized vol (annualized)
    All are oriented so higher = more stress.
    """
    if "vix_close" not in market.columns:
        raise ValueError("market must include vix_close")

    close_col = f"close_{equity_ticker.upper()}"
    if close_col not in market.columns:
        raise ValueError(f"market must include {close_col}")

    out = pd.DataFrame(index=market.index)
    out["vix_level"] = market["vix_close"].astype(float)
    out["vix_log_change"] = np.log(out["vix_level"]).diff()

    prices = market[[close_col]].rename(columns={close_col: "equity"})
    r = log_returns_from_prices(prices)["equity"]

    out["rv_20"] = r.rolling(20).std(ddof=0) * np.sqrt(252)
    out["rv_60"] = r.rolling(60).std(ddof=0) * np.sqrt(252)

    return out
