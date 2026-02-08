import pandas as pd
from src.setups.trend_analyzer import TrendAnalyzer

def test_uptrend_detection():
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=50),
        "close": [100 + i for i in range(50)],
        "ema_20": [95 + i for i in range(50)],
        "ema_50": [90 + i for i in range(50)],
        "ema_200": [85 + i for i in range(50)],
        "rsi_14": [60] * 50
    })

    analyzer = TrendAnalyzer("config/trend_rules.json")
    result = analyzer.analyze(df)

    assert result["trend"] == "UP"
    assert result["strength"] == "STRONG"
