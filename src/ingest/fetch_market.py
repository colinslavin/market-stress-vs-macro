from __future__ import annotations

import pandas as pd
import yfinance as yf

def _flatten_yf_multiindex(df: pd.DataFrame) -> pd.DataFrame:
    """
    yfinance returns MultiIndex columns for multiple tickers: (field, ticker) or (ticker, field).
    Normalize to columns like close_SPY, volume_XLK, etc.
    Also handles the case where columns are tuples but not a pd.MultiIndex.
    """
    # tuple columns but not MultiIndex -> coerce
    if not isinstance(df.columns, pd.MultiIndex) and len(df.columns) > 0 and isinstance(df.columns[0], tuple):
        df.columns = pd.MultiIndex.from_tuples(df.columns)

    if not isinstance(df.columns, pd.MultiIndex):
        df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]
        return df

    level0 = [str(x).lower() for x in df.columns.get_level_values(0)]
    fields = {"open", "high", "low", "close", "adj close", "adj_close", "volume"}

    if any(f in fields for f in level0):
        # (field, ticker)
        df.columns = [
            f"{str(f).lower().replace(' ', '_')}_{str(t).upper()}"
            for f, t in df.columns
        ]
        return df

    # assume (ticker, field)
    df.columns = [
        f"{str(f).lower().replace(' ', '_')}_{str(t).upper()}"
        for t, f in df.columns
    ]
    return df



def fetch_market_data(
    start: str,
    end: str | None,
    panel_tickers: tuple[str, ...] = ("SPY",),
    vix_ticker: str = "^VIX",
) -> pd.DataFrame:
    """
    Fetch daily market series for stress indicators:
    - Panel tickers: close + volume (sector ETF panel)
    - VIX close

    No feature engineering here. Raw-ish series only.
    """
    tickers = list(panel_tickers)
    panel = yf.download(tickers, start=start, end=end, auto_adjust=False, progress=False, group_by="column")
    if panel.empty:
        raise ValueError(f"No data returned for panel tickers: {tickers}")

    panel = _flatten_yf_multiindex(panel)

    # Extract close + volume columns for the panel
    close_cols = [c for c in panel.columns if c.startswith("close_")]
    vol_cols   = [c for c in panel.columns if c.startswith("volume_")]

    panel = panel[close_cols + vol_cols].copy()

    # Fetch VIX
    vix = yf.download(vix_ticker, start=start, end=end, auto_adjust=False, progress=False, group_by="column")
    if vix.empty:
        raise ValueError(f"No data returned for {vix_ticker}")

    vix = _flatten_yf_multiindex(vix)

    # Robustly find VIX close regardless of how yfinance labeled it
    vix_close_candidates = [c for c in vix.columns if c == "close" or c.startswith("close_")]
    if not vix_close_candidates:
        raise ValueError(f"Could not find a close column for {vix_ticker}. Got columns: {list(vix.columns)[:20]}")

    vix_close_col = "close" if "close" in vix.columns else vix_close_candidates[0]
    vix = vix.rename(columns={vix_close_col: "vix_close"})[["vix_close"]]

    # Join on calendar intersection
    df = panel.join(vix, how="inner")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index().dropna(how="any")  # strict: keep clean intersection

    return df
