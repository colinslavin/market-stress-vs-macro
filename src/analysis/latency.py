from __future__ import annotations
import pandas as pd


def first_trigger_date(
    series: pd.Series,
    threshold: float,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> pd.Timestamp | None:
    window = series.loc[start:end]
    hits = window[window >= threshold]
    if hits.empty:
        return None
    return hits.index[0]


def compute_latency_table(
    events: pd.DataFrame,
    csi: pd.Series,
    macro_regime: pd.Series,
) -> pd.DataFrame:
    """
    Compute detection latency relative to event start.
    """
    rows = []

    for _, ev in events.iterrows():
        start, end = ev["start"], ev["end"]

        csi_trigger = first_trigger_date(
            csi,
            threshold=csi.quantile(0.95),
            start=start,
            end=end,
        )

        macro_trigger = first_trigger_date(
            macro_regime,
            threshold=1,  # macro "risk on/off" threshold
            start=start,
            end=end,
        )

        rows.append({
            "event": ev["label"],
            "type": ev["type"],
            "csi_days_to_trigger": (csi_trigger - start).days if csi_trigger else None,
            "macro_days_to_trigger": (macro_trigger - start).days if macro_trigger else None,
        })

    return pd.DataFrame(rows)
