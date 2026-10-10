"""Book datasets, loaded as Polars DataFrames.

The same tables R4DS uses — `palmerpenguins` and `nycflights13` — read straight
from the CSV files those PyPI packages ship. The packages themselves are never
imported: `nycflights13`'s ``__init__`` eagerly loads every table with pandas.

Examples
--------
```python
from pl_notes import datasets

penguins_df_raw = datasets.penguins()
flights_df_raw = datasets.flights()
```
"""

import importlib.util
import zipfile
from pathlib import Path

import polars as pl

__all__ = ["penguins", "flights", "airlines", "airports", "planes", "weather"]

_NA = "NA"
# Infer dtypes from every row, not the first 100: weather.precip starts as all 0s.
_CSV_OPTS = {"null_values": _NA, "infer_schema_length": None}
_NYC_TZ = "America/New_York"


def penguins() -> pl.DataFrame:
    """Palmer penguins, 344 × 8 (`palmerpenguins::penguins`; factors as String)."""
    return pl.read_csv(_data_dir("palmerpenguins") / "penguins.csv", **_CSV_OPTS)


def flights() -> pl.DataFrame:
    """All flights departing NYC in 2013, 336,776 × 19 (`nycflights13::flights`).

    Row order is the package CSV's, not R's: months run 1, 10, 11, 12, 2, …
    Sort before relying on "first" rows.
    """
    with zipfile.ZipFile(_data_dir("nycflights13") / "flights.csv.zip") as zf:
        csv_bytes = zf.read("flights.csv")
    return pl.read_csv(csv_bytes, **_CSV_OPTS).pipe(_parse_time_hour)


def airlines() -> pl.DataFrame:
    """Airline names by carrier code, 16 × 2 (`nycflights13::airlines`)."""
    return _read_nycflights13("airlines")


def airports() -> pl.DataFrame:
    """Airport metadata by FAA code, 1,458 × 8 (`nycflights13::airports`)."""
    return _read_nycflights13("airports")


def planes() -> pl.DataFrame:
    """Plane metadata by tail number, 3,322 × 9 (`nycflights13::planes`)."""
    return _read_nycflights13("planes")


def weather() -> pl.DataFrame:
    """Hourly weather at each NYC origin, 26,115 × 15 (`nycflights13::weather`)."""
    return _read_nycflights13("weather").pipe(_parse_time_hour)


def _read_nycflights13(name: str) -> pl.DataFrame:
    return pl.read_csv(_data_dir("nycflights13") / f"{name}.csv", **_CSV_OPTS)


def _parse_time_hour(df: pl.DataFrame) -> pl.DataFrame:
    # Stored as UTC ISO strings; R's tibble shows the same instant in New York time.
    return df.with_columns(
        pl.col("time_hour")
        .str.to_datetime("%Y-%m-%dT%H:%M:%SZ", time_zone="UTC")
        .dt.convert_time_zone(_NYC_TZ)
    )


def _data_dir(package: str) -> Path:
    # find_spec locates the package without executing its __init__.
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ModuleNotFoundError(f"{package} is not installed: run `uv sync`")
    return Path(next(iter(spec.submodule_search_locations))) / "data"
