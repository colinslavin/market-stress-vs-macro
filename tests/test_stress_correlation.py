import numpy as np
import pandas as pd
from src.features.stress_correlation import compute_correlation_stress

def test_corr_bounds():
    idx = pd.date_range("2020-01-01", periods=120, freq="D")
    # create simple price series
    base = np.cumprod(1 + 0.001*np.random.default_rng(0).normal(size=len(idx)))
    market = pd.DataFrame({
        "close_SPY": 100*base,
        "close_XLK": 50*base*(1+0.0001),
        "close_XLF": 30*base*(1-0.0001),
        "close_XLE": 40*base*(1+0.0002),
        "vix_close": 20.0,
        "volume_SPY": 1.0
    }, index=idx)

    s = compute_correlation_stress(market, window=20)
    assert ((s.dropna() >= -1.0001) & (s.dropna() <= 1.0001)).all()
