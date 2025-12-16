from __future__ import annotations

import pandas as pd
from utils.io import load_parquet, save_parquet
from regimes.stress_index import (
    build_composite_stress_index,
    classify_stress_regimes,
)


def main() -> None:
    stress = load_parquet("processed/stress_indicators.parquet")

    csi = build_composite_stress_index(stress, window=120)
    regime = classify_stress_regimes(csi)

    out = pd.concat([stress, csi, regime], axis=1)
    save_parquet(out, "processed/csi.parquet")

    print("Saved: data/processed/csi.parquet")
    print(out[["CSI", "stress_regime"]].tail())


if __name__ == "__main__":
    main()
