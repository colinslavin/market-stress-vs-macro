from __future__ import annotations

import pandas as pd
from pandas_datareader import data as pdr


def _to_monthly_period_index(s: pd.Series) -> pd.Series:
    # Ensure monthly series indexed by timestamp; many FRED series are month-end.
    s.index = pd.to_datetime(s.index)
    return s.sort_index()


def fetch_macro_monthly_fred(
    series_ids: tuple[str, ...],
    start: str,
    end: str | None,
) -> pd.DataFrame:
    """
    Fetch monthly macro series from FRED.

    Returns a monthly-indexed DataFrame (timestamp index).
    No lag applied here.
    """
    frames = []
    for sid in series_ids:
        s = pdr.DataReader(sid, "fred", start, end)
        s.columns = [sid]
        s[sid] = pd.to_numeric(s[sid], errors="coerce")
        frames.append(_to_monthly_period_index(s[sid]))

    df = pd.concat(frames, axis=1).dropna(how="all").sort_index()
    return df


def apply_publication_lag_and_daily_ffill(
    macro_monthly: pd.DataFrame,
    start: str,
    end: str | None,
    publication_lag_days: int = 35,
) -> pd.DataFrame:
    """
    Convert monthly macro to a daily series with explicit "availability lag".

    Interpretation:
    - A monthly observation dated at month-end is only known after `publication_lag_days`.
    - Before the "release date", it must NOT be visible (NaN).
    - After release, it is forward-filled daily until the next release.

    This is conservative and avoids lookahead.
    """
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end) if end is not None else pd.Timestamp.today().normalize()

    # Macro monthly timestamps -> "available" timestamps
    available_index = (macro_monthly.index + pd.Timedelta(days=publication_lag_days))
    macro_available = macro_monthly.copy()
    macro_available.index = available_index
    macro_available = macro_available.sort_index()

    # Create daily index and reindex
    daily_index = pd.date_range(start_dt, end_dt, freq="D")
    daily = macro_available.reindex(daily_index)

    # Forward-fill AFTER availability only
    daily = daily.ffill()

    return daily


def fetch_macro_data_daily(
    series_ids: tuple[str, ...],
    start: str,
    end: str | None,
    publication_lag_days: int = 35,
    fetch_buffer_days: int = 180,
) -> pd.DataFrame:
    """
    Full macro pipeline: FRED monthly -> apply lag -> daily ffill.

    We fetch extra history BEFORE `start` so that after applying publication lag
    the daily macro series is already available at the beginning of the market window.
    This avoids initial NaNs without introducing lookahead.
    """
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end) if end is not None else pd.Timestamp.today().normalize()

    buffered_start_dt = start_dt - pd.Timedelta(days=fetch_buffer_days)
    buffered_start = buffered_start_dt.strftime("%Y-%m-%d")

    monthly = fetch_macro_monthly_fred(series_ids, buffered_start, end)
    daily = apply_publication_lag_and_daily_ffill(
        monthly,
        buffered_start,
        end,
        publication_lag_days,
    )

    # Slice back to requested window
    daily = daily.loc[start_dt:end_dt]

    return daily
