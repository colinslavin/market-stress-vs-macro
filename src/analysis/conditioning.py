from __future__ import annotations
import pandas as pd
import numpy as np

def conditional_forward_metrics(
    returns: pd.Series,
    regime: pd.Series,
    horizon: int = 20,
) -> pd.DataFrame:
    """
    Compute forward risk metrics conditional on regime.
    """
    out = []

    for r in sorted(regime.dropna().unique()):
        idx = regime[regime == r].index
        fwd = returns.shift(-horizon).loc[idx]

        out.append({
            "regime": r,
            "mean_fwd_return": fwd.mean(),
            "fwd_vol": fwd.std(),
            "downside_prob": (fwd < 0).mean(),
        })

    return pd.DataFrame(out)
