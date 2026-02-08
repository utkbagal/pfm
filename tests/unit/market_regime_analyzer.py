import pandas as pd
from src.intelligence.market_regime_analyzer import MarketRegimeAnalyzer

def test_bullish_regime():
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=50),
        "close": [100 + i for i in range(50)],
        "ema_20": [90 + i for i in range(50)],
        "ema_50": [85 + i for i in range(50)],
        "ema_200": [80 + i for i in range(50)],
        "atr_14": [1.2] * 50
    })

    analyzer = MarketRegimeAnalyzer(
        "config/market_regime_rules.json"
    )

    result = analyzer.analyze(df)
    assert result["regime"] == "BULLISH"
