import pandas as pd
from src.features.stress_volume import compute_volume_stress

def test_volume_ratio_zero_when_constant_after_window():
    idx = pd.date_range("2020-01-01", periods=100, freq="D")
    market = pd.DataFrame({
        "volume_SPY": [100.0]*100,
        "close_SPY": [100.0]*100,
        "vix_close": [20.0]*100,
    }, index=idx)

    out = compute_volume_stress(market, equity_ticker="SPY")
    # After rolling window fills, log(volume/median)=0
    assert abs(out["vol_log_ratio_20"].dropna().iloc[-1]) < 1e-9
    assert abs(out["vol_log_ratio_60"].dropna().iloc[-1]) < 1e-9
