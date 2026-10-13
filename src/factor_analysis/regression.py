"""Estimation des modèles factoriels.

Modèle : r_t - rf_t = alpha + beta_1 F_1t + ... + beta_k F_kt + eps_t

On estime par OLS, mais avec des erreurs standard robustes (Newey-West / HAC)
car les résidus de séries financières sont souvent hétéroscédastiques et
autocorrélés.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

CAPM = ["Mkt-RF"]
FF3 = ["Mkt-RF", "SMB", "HML"]
FF5 = ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]
MODELS = {"CAPM": CAPM, "FF3": FF3, "FF5": FF5}


def fit_factor_model(
    excess_returns: pd.Series,
    factors: pd.DataFrame,
    factor_cols: list[str],
    hac_lags: int | None = 6,
):
    """Régression OLS d'un rendement excédentaire sur des facteurs.

    Si hac_lags est None, on utilise les erreurs standard OLS classiques ;
    sinon, des erreurs Newey-West avec ce nombre de retards.
    """
    data = pd.concat([excess_returns.rename("y"), factors[factor_cols]], axis=1).dropna()
    y = data["y"]
    X = sm.add_constant(data[factor_cols])
    model = sm.OLS(y, X)
    if hac_lags is None:
        return model.fit()
    return model.fit(cov_type="HAC", cov_kwds={"maxlags": hac_lags})


def compare_models(
    excess_returns: pd.Series,
    factors: pd.DataFrame,
    hac_lags: int | None = 6,
) -> pd.DataFrame:
    """Compare CAPM, FF3 et FF5 sur un même actif.

    Retourne, pour chaque modèle : alpha, t-stat de l'alpha, R² ajusté, AIC, BIC.
    """
    rows = {}
    for name, cols in MODELS.items():
        res = fit_factor_model(excess_returns, factors, cols, hac_lags)
        rows[name] = {
            "alpha": res.params["const"],
            "t_alpha": res.tvalues["const"],
            "r2_adj": res.rsquared_adj,
            "aic": res.aic,
            "bic": res.bic,
            "n_obs": int(res.nobs),
        }
    return pd.DataFrame(rows).T


def rolling_betas(
    excess_returns: pd.Series,
    factors: pd.DataFrame,
    factor_cols: list[str],
    window: int = 60,
) -> pd.DataFrame:
    """Coefficients OLS estimés sur une fenêtre glissante de `window` mois.

    Retourne un DataFrame indexé par la date de fin de fenêtre, avec une
    colonne par coefficient (const + facteurs).
    """
    data = pd.concat([excess_returns.rename("y"), factors[factor_cols]], axis=1).dropna()
    if len(data) < window:
        raise ValueError("Pas assez d'observations pour la fenêtre demandée.")

    y = data["y"].to_numpy()
    X = np.column_stack([np.ones(len(data)), data[factor_cols].to_numpy()])
    columns = ["const", *factor_cols]

    out = []
    for end in range(window, len(data) + 1):
        coef, *_ = np.linalg.lstsq(X[end - window : end], y[end - window : end], rcond=None)
        out.append(coef)

    return pd.DataFrame(out, index=data.index[window - 1 :], columns=columns)
