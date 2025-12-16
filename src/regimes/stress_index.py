from __future__ import annotations
import pandas as pd
from features.stress_utils import rolling_zscore


DEFAULT_WINDOWS = {
    "short": 20,
    "medium": 60,
    "long": 120,
}


def build_normalized_stress_components(
    stress: pd.DataFrame,
    window: int = 120,
) -> pd.DataFrame:
    """
    Normalize stress indicators using rolling z-scores.

    Higher values must correspond to more stress.
    """
    z = {}
    for col in stress.columns:
        z[col] = rolling_zscore(stress[col], window=window)

    z_df = pd.DataFrame(z)
    return z_df


def build_composite_stress_index(
    stress: pd.DataFrame,
    window: int = 120,
) -> pd.Series:
    """
    Build Composite Stress Index (CSI).

    Method:
    - rolling z-score each indicator
    - equal-weight average across indicators
    """
    z = build_normalized_stress_components(stress, window=window)

    csi = z.mean(axis=1)
    csi.name = "CSI"
    return csi

def classify_stress_regimes(
    csi: pd.Series,
    p_elevated: float = 0.85,
    p_crisis: float = 0.95,
) -> pd.Series:
    """
    Classify CSI into stress regimes using expanding percentiles.

    Regimes:
    - 0: Normal
    - 1: Elevated
    - 2: Crisis
    """
    regimes = []

    for t in range(len(csi)):
        hist = csi.iloc[: t + 1].dropna()
        if len(hist) < 50:
            regimes.append(pd.NA)
            continue

        q_e = hist.quantile(p_elevated)
        q_c = hist.quantile(p_crisis)

        val = csi.iloc[t]
        if val >= q_c:
            regimes.append(2)
        elif val >= q_e:
            regimes.append(1)
        else:
            regimes.append(0)

    return pd.Series(regimes, index=csi.index, name="stress_regime")
