import pandas as pd
import pytest

from factor_analysis import parse_french_csv

SAMPLE = """This file was created by CMPT_ME_BEME_RETS using the 202509 CRSP database.

,Mkt-RF,SMB,HML,RMW,CMA,RF
196307,   -0.39,   -0.46,   -0.81,    0.72,   -1.16,    0.27
196308,    5.08,   -0.80,    1.70,    0.40,   -0.38,    0.25

 Annual Factors: January-December
,Mkt-RF,SMB,HML,RMW,CMA,RF
1964,   12.44,   -1.18,    8.78,    1.51,    5.32,    3.54
"""


def test_parse_keeps_only_monthly_table_in_decimals():
    df = parse_french_csv(SAMPLE)
    assert len(df) == 2
    assert list(df.columns) == ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "RF"]
    assert df.index[0] == pd.Period("1963-07", freq="M")
    assert df.loc[pd.Period("1963-08", freq="M"), "Mkt-RF"] == pytest.approx(0.0508)


def test_parse_raises_on_garbage():
    with pytest.raises(ValueError):
        parse_french_csv("rien d'utile ici")
