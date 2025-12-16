from __future__ import annotations
import pandas as pd


def define_stress_events() -> pd.DataFrame:
    """
    Define major stress episodes for evaluation.

    Classification:
    - sudden: fast onset, fast resolution
    - prolonged: slow burn, persistent stress
    """
    events = [
        # Sudden shocks
        ("2008-09-15", "2008-11-30", "sudden", "GFC shock"),
        ("2010-05-01", "2010-06-30", "sudden", "Flash Crash"),
        ("2020-02-15", "2020-04-30", "sudden", "COVID shock"),

        # Prolonged stress
        ("2007-07-01", "2009-06-30", "prolonged", "GFC prolonged"),
        ("2011-07-01", "2012-06-30", "prolonged", "Euro debt"),
        ("2022-01-01", "2022-12-31", "prolonged", "Tightening cycle"),
    ]

    df = pd.DataFrame(events, columns=["start", "end", "type", "label"])
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    return df
