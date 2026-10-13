"""Analyse factorielle Fama-French par régression."""

from .data import get_monthly_returns, load_ff_factors, parse_french_csv
from .regression import compare_models, fit_factor_model, rolling_betas

__all__ = [
    "get_monthly_returns",
    "load_ff_factors",
    "parse_french_csv",
    "compare_models",
    "fit_factor_model",
    "rolling_betas",
]
