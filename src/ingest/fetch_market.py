import pandas as pd
import yfinance as yf

def _flatten_cols(cols):
    # yfinance may return MultiIndex columns like ('Close', 'SPY')
    if isinstance(cols, pd.MultiIndex):
        return [str(c[0]) for c in cols.to_list()]
    # sometimes it’s already tuples
    return [str(c[0]) if isinstance(c, tuple) else str(c) for c in cols]

def fetch_market_data(start, end, equity_ticker="SPY", vix_ticker="^VIX") -> pd.DataFrame:
    eq = yf.download(equity_ticker, start=start, end=end, auto_adjust=False, progress=False)
    if eq.empty:
        raise ValueError(f"No data returned for {equity_ticker}. Check ticker or network.")

    eq.columns = [c.lower().replace(" ", "_") for c in _flatten_cols(eq.columns)]
    eq = eq.rename(columns={
        "adj_close": "adj_close_equity",
        "close": "close_equity",
        "volume": "volume_equity",
    })

    vix = yf.download(vix_ticker, start=start, end=end, auto_adjust=False, progress=False)
    if vix.empty:
        raise ValueError(f"No data returned for {vix_ticker}. Check ticker or network.")

    vix.columns = [c.lower().replace(" ", "_") for c in _flatten_cols(vix.columns)]
    vix = vix.rename(columns={"close": "vix_close"})

    df = eq[["close_equity", "volume_equity"]].join(vix[["vix_close"]], how="inner")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index().dropna()

    return df
