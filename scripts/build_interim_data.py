from __future__ import annotations

from src.config import DATA, MARKET, MACRO
from src.ingest.fetch_market import fetch_market_data
from src.ingest.fetch_macro import fetch_macro_data_daily
from src.features.preprocess import align_daily_market_and_macro
from src.utils.io import save_parquet


def main() -> None:
    start, end = DATA.start, DATA.end

    market = fetch_market_data(
        start=start,
        end=end,
        panel_tickers=MARKET.panel_tickers,
        vix_ticker=MARKET.ticker_vix,
    )

    macro = fetch_macro_data_daily(
        series_ids=MACRO.series,
        start=start,
        end=end,
        publication_lag_days=MACRO.publication_lag_days,
    )

    market_aligned, macro_aligned = align_daily_market_and_macro(market, macro)

    save_parquet(market_aligned, "interim/market_daily.parquet")
    save_parquet(macro_aligned, "interim/macro_daily.parquet")

    print("Saved:")
    print(" - data/interim/market_daily.parquet", market_aligned.shape)
    print(" - data/interim/macro_daily.parquet", macro_aligned.shape)


if __name__ == "__main__":
    main()
