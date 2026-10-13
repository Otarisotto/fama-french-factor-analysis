"""Téléchargement et préparation des données.

Deux sources :
- les facteurs Fama-French (site de Kenneth French, gratuit) ;
- les prix des actifs via yfinance.

Tous les rendements sont mensuels et exprimés en décimales (0.01 = 1 %).
"""

from __future__ import annotations

import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

FF5_URL = (
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
    "F-F_Research_Data_5_Factors_2x3_CSV.zip"
)
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def parse_french_csv(text: str) -> pd.DataFrame:
    """Extrait la table mensuelle d'un fichier CSV de Kenneth French.

    Le fichier contient d'abord une table mensuelle, puis une table annuelle.
    On ne garde que la partie mensuelle, et on convertit les pourcentages
    en décimales. L'index est une PeriodIndex mensuelle.
    """
    header: list[str] | None = None
    rows: list[list[str]] = []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        first = parts[0]
        if header is None:
            if first == "" and "Mkt-RF" in parts:
                header = parts[1:]
            continue
        if first.isdigit() and len(first) == 6:
            rows.append(parts)
        elif rows:
            break  # fin de la table mensuelle

    if header is None or not rows:
        raise ValueError("Table mensuelle introuvable dans le fichier fourni.")

    df = pd.DataFrame(
        [r[1 : 1 + len(header)] for r in rows],
        columns=header,
        index=pd.PeriodIndex([r[0] for r in rows], freq="M"),
    ).astype(float)
    return df / 100.0


def load_ff_factors(refresh: bool = False) -> pd.DataFrame:
    """Charge les 5 facteurs Fama-French mensuels (Mkt-RF, SMB, HML, RMW, CMA, RF).

    Le résultat est mis en cache dans data/raw/ pour ne télécharger qu'une fois.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cache = RAW_DIR / "ff5_monthly.csv"

    if cache.exists() and not refresh:
        df = pd.read_csv(cache, index_col=0)
        df.index = pd.PeriodIndex(df.index, freq="M")
        return df

    with urllib.request.urlopen(FF5_URL, timeout=60) as response:
        payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        name = archive.namelist()[0]
        text = archive.read(name).decode("latin-1")

    df = parse_french_csv(text)
    df.to_csv(cache)
    return df


def get_monthly_returns(tickers: list[str], start: str, end: str | None = None) -> pd.DataFrame:
    """Rendements mensuels (prix ajustés) pour une liste de tickers.

    Exemple : get_monthly_returns(["AAPL", "MSFT"], start="2010-01-01")
    """
    import yfinance as yf  # import ici pour que les tests n'en dépendent pas

    prices = yf.download(
        tickers, start=start, end=end, auto_adjust=True, progress=False
    )["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(tickers[0])

    monthly = prices.groupby(prices.index.to_period("M")).last()
    return monthly.pct_change().dropna(how="all")
