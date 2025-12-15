from __future__ import annotations

import pandas as pd


def align_daily_market_and_macro(
    market_daily: pd.DataFrame,
    macro_daily: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Align market and macro datasets to a common daily index.

    Rules:
    - Market drives the calendar (only days where market exists are kept).
    - Macro must not introduce extra dates; it is reindexed onto market dates.
    - No feature engineering here.
    """
    market_daily = market_daily.copy()
    macro_daily = macro_daily.copy()

    market_daily.index = pd.to_datetime(market_daily.index)
    macro_daily.index = pd.to_datetime(macro_daily.index)

    market_daily = market_daily.sort_index()
    macro_daily = macro_daily.sort_index()

    # Reindex macro to market days (never the other way around)
    macro_aligned = macro_daily.reindex(market_daily.index).ffill()

    # The only acceptable NaNs in macro_aligned are at the very beginning
    # before first available release; keep them (they’re correct).
    return market_daily, macro_aligned
