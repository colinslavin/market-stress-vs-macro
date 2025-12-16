import numpy as np
import pandas as pd
from src.features.stress_dispersion import compute_dispersion_stress

def test_dispersion_nonnegative():
    idx = pd.date_range("2020-01-01", periods=100, freq="D")
    rng = np.random.default_rng(1)
    prices = {
        "close_SPY": 100*np.cumprod(1 + 0.001*rng.normal(size=len(idx))),
        "close_XLK":  50*np.cumprod(1 + 0.001*rng.normal(size=len(idx))),
        "close_XLF":  30*np.cumprod(1 + 0.001*rng.normal(size=len(idx))),
        "close_XLE":  40*np.cumprod(1 + 0.001*rng.normal(size=len(idx))),
        "vix_close": 20.0,
        "volume_SPY": 1.0,
    }
    market = pd.DataFrame(prices, index=idx)
    disp = compute_dispersion_stress(market, window=10)
    assert (disp.dropna() >= 0).all()
