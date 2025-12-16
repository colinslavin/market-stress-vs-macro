from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class MarketConfig:
    ticker_equity: str = "SPY"
    ticker_vix: str = "^VIX"

    # Small liquid panel for cross-sectional correlation/dispersion proxies
    # (reproducible; no constituent dataset needed)
    panel_tickers = (
        "SPY",
        "XLB", "XLE", "XLF", "XLI", "XLK",
        "XLP", "XLU", "XLV", "XLY",
    )


@dataclass(frozen=True)
class MacroConfig:
    # Keep macro minimal & interpretable
    # FRED series IDs:
    # - CPIAUCSL: CPI (inflation)
    # - INDPRO: Industrial Production Index (growth proxy)
    series: tuple[str, ...] = ("CPIAUCSL", "INDPRO")

    # Conservative "availability" rule:
    # monthly value released with delay, available after X calendar days
    publication_lag_days: int = 35


@dataclass(frozen=True)
class DataConfig:
    start: str = "2000-01-01"
    end: str | None = None  # None -> up to today
    base_frequency: str = "D"  # daily


MARKET = MarketConfig()
MACRO = MacroConfig()
DATA = DataConfig()
