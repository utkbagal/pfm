import pandas as pd
from src.intelligence.liquidity_volatility_filter import (
    LiquidityVolatilityFilter
)

def test_liquidity_filter_pass():
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=30),
        "close": [100] * 30,
        "atr_14": [1.5] * 30,
        "vol_avg_20": [1_000_000] * 30
    })

    filter_ = LiquidityVolatilityFilter(
        "config/liquidity_rules.json"
    )

    result = filter_.evaluate({"TEST": df})
    assert result["TEST"]["tradable"] is True
