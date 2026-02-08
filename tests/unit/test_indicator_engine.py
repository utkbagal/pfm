import pandas as pd
from src.data_layer.indicator_engine import IndicatorEngine

def test_indicators_added():
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=30),
        "open": range(30),
        "high": range(1, 31),
        "low": range(30),
        "close": range(1, 31),
        "volume": range(100, 130)
    })

    engine = IndicatorEngine()
    result = engine.compute({"TEST": df})

    out = result["TEST"]

    assert "ema_20" in out.columns
    assert "rsi_14" in out.columns
    assert "atr_14" in out.columns
    assert "bb_upper" in out.columns
