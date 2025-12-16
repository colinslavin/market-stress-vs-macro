from __future__ import annotations
import numpy as np
import pandas as pd


def compute_volume_stress(market: pd.DataFrame, equity_ticker: str = "SPY") -> pd.DataFrame:
    """
    Liquidity / forced participation proxy using volume anomalies.

    Output:
    - vol_log_ratio_20: log(volume / rolling_median_20)
    - vol_log_ratio_60: log(volume / rolling_median_60)
    Higher = more stress.
    """
    vol_col = f"volume_{equity_ticker.upper()}"
    if vol_col not in market.columns:
        raise ValueError(f"market must include {vol_col}")

    v = market[vol_col].astype(float)
    out = pd.DataFrame(index=market.index)

    med20 = v.rolling(20).median()
    med60 = v.rolling(60).median()

    out["vol_log_ratio_20"] = np.log(v / med20)
    out["vol_log_ratio_60"] = np.log(v / med60)

    return out
