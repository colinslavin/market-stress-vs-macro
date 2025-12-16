from __future__ import annotations

import pandas as pd

from src.utils.io import load_parquet, save_parquet
from src.features.stress_volatility import compute_volatility_indicators
from src.features.stress_volume import compute_volume_stress
from src.features.stress_correlation import compute_correlation_stress
from src.features.stress_dispersion import compute_dispersion_stress
from src.features.stress_tails import compute_tail_stress


def main() -> None:
    market = load_parquet("interim/market_daily.parquet")

    vol = compute_volatility_indicators(market, equity_ticker="SPY")
    volu = compute_volume_stress(market, equity_ticker="SPY")

    corr_60 = compute_correlation_stress(market, window=60).reindex(market.index)
    corr_20 = compute_correlation_stress(market, window=20).reindex(market.index)

    disp_20 = compute_dispersion_stress(market, window=20)
    disp_60 = compute_dispersion_stress(market, window=60)

    tail = compute_tail_stress(market, equity_ticker="SPY", window=252, q=0.05)

    out = pd.concat(
        [
            vol,
            volu,
            corr_20.rename("avg_pairwise_corr_20"),
            corr_60.rename("avg_pairwise_corr_60"),
            disp_20.rename("xsec_dispersion_20"),
            disp_60.rename("xsec_dispersion_60"),
            tail,
        ],
        axis=1,
    )

    save_parquet(out, "processed/stress_indicators.parquet")
    print("Saved: data/processed/stress_indicators.parquet", out.shape)
    print(out.tail())


if __name__ == "__main__":
    main()
