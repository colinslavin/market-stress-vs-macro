from __future__ import annotations

import pandas as pd

from ingest.fetch_macro import apply_publication_lag_and_daily_ffill
from features.preprocess import align_daily_market_and_macro


def test_macro_lag_prevents_early_visibility():
    # Construct a toy monthly macro series with a single observation at month-end
    monthly_idx = pd.to_datetime(["2020-01-31", "2020-02-29"])
    macro_monthly = pd.DataFrame({"CPIAUCSL": [100.0, 101.0]}, index=monthly_idx)

    daily = apply_publication_lag_and_daily_ffill(
        macro_monthly,
        start="2020-01-01",
        end="2020-03-15",
        publication_lag_days=35,
    )

    # The Jan value should not appear until 2020-01-31 + 35 days = 2020-03-06
    assert pd.isna(daily.loc["2020-03-01", "CPIAUCSL"])
    assert daily.loc["2020-03-06", "CPIAUCSL"] == 100.0


def test_align_uses_market_calendar():
    market_idx = pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-06"])  # trading days
    market = pd.DataFrame({"close_equity": [1, 2, 3], "volume_equity": [10, 11, 12], "vix_close": [20, 21, 19]}, index=market_idx)

    macro_idx = pd.date_range("2020-01-01", "2020-01-10", freq="D")
    macro = pd.DataFrame({"CPIAUCSL": range(len(macro_idx))}, index=macro_idx)

    mkt_aligned, macro_aligned = align_daily_market_and_macro(market, macro)

    assert mkt_aligned.index.equals(market_idx)
    assert macro_aligned.index.equals(market_idx)
