import numpy as np
import pandas as pd
from src.features.stress_volatility import compute_volatility_indicators

def test_vix_log_change_matches_diff():
    idx = pd.date_range("2020-01-01", periods=5, freq="D")
    market = pd.DataFrame({
        "vix_close": [10, 11, 12.1, 12.1, 9.9],
        "close_SPY": [100, 101, 102, 101, 99],
        "volume_SPY": [1, 1, 1, 1, 1],
    }, index=idx)

    out = compute_volatility_indicators(market, equity_ticker="SPY")
    expected = np.log(pd.Series([10,11,12.1,12.1,9.9], index=idx)).diff()
    pd.testing.assert_series_equal(out["vix_log_change"], expected.rename("vix_log_change"), check_names=False)
