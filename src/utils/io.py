from __future__ import annotations

from pathlib import Path
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]  # .../src/utils/io.py -> repo root


def data_dir() -> Path:
    return REPO_ROOT / "data"


def ensure_dirs() -> None:
    for p in [data_dir() / "raw", data_dir() / "interim", data_dir() / "processed", REPO_ROOT / "reports" / "figures"]:
        p.mkdir(parents=True, exist_ok=True)


def save_parquet(df: pd.DataFrame, rel_path: str) -> Path:
    ensure_dirs()
    path = data_dir() / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=True)
    return path


def load_parquet(rel_path: str) -> pd.DataFrame:
    path = data_dir() / rel_path
    return pd.read_parquet(path)
