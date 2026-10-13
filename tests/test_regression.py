"""Tests sur données synthétiques : on connaît les vrais coefficients,
donc on peut vérifier que le code les retrouve."""

import numpy as np
import pandas as pd
import pytest

from factor_analysis import compare_models, fit_factor_model, rolling_betas

TRUE_ALPHA = 0.002
TRUE_BETAS = {"Mkt-RF": 1.1, "SMB": 0.4, "HML": -0.3}


@pytest.fixture
def synthetic():
    rng = np.random.default_rng(42)
    n = 1500
    index = pd.period_range("1900-01", periods=n, freq="M")
    factors = pd.DataFrame(
        rng.normal(0, 0.04, size=(n, 5)),
        columns=["Mkt-RF", "SMB", "HML", "RMW", "CMA"],
        index=index,
    )
    noise = rng.normal(0, 0.01, size=n)
    y = TRUE_ALPHA + sum(b * factors[k] for k, b in TRUE_BETAS.items()) + noise
    return y.rename("asset"), factors


def test_fit_recovers_true_coefficients(synthetic):
    y, factors = synthetic
    res = fit_factor_model(y, factors, ["Mkt-RF", "SMB", "HML"])
    assert res.params["const"] == pytest.approx(TRUE_ALPHA, abs=0.001)
    for name, beta in TRUE_BETAS.items():
        assert res.params[name] == pytest.approx(beta, abs=0.03)


def test_hac_and_classic_give_same_coefficients(synthetic):
    y, factors = synthetic
    cols = ["Mkt-RF", "SMB", "HML"]
    hac = fit_factor_model(y, factors, cols, hac_lags=6)
    ols = fit_factor_model(y, factors, cols, hac_lags=None)
    np.testing.assert_allclose(hac.params, ols.params)  # même estimateur
    assert not np.allclose(hac.bse, ols.bse)  # mais erreurs standard différentes


def test_compare_models_prefers_true_model_over_capm(synthetic):
    y, factors = synthetic
    table = compare_models(y, factors)
    assert list(table.index) == ["CAPM", "FF3", "FF5"]
    assert table.loc["FF3", "r2_adj"] > table.loc["CAPM", "r2_adj"]
    assert table.loc["FF3", "bic"] < table.loc["CAPM", "bic"]


def test_rolling_betas_shape_and_values(synthetic):
    y, factors = synthetic
    cols = ["Mkt-RF", "SMB"]
    window = 60
    betas = rolling_betas(y, factors, cols, window=window)
    assert betas.shape == (len(y) - window + 1, 1 + len(cols))
    assert list(betas.columns) == ["const", "Mkt-RF", "SMB"]
    # la dernière fenêtre doit coïncider avec une régression directe
    direct = fit_factor_model(y.iloc[-window:], factors.iloc[-window:], cols, hac_lags=None)
    np.testing.assert_allclose(betas.iloc[-1].to_numpy(), direct.params.to_numpy())


def test_rolling_betas_rejects_short_sample(synthetic):
    y, factors = synthetic
    with pytest.raises(ValueError):
        rolling_betas(y.iloc[:10], factors.iloc[:10], ["Mkt-RF"], window=60)
