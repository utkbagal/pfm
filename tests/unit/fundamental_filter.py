from src.intelligence.fundamental_filter import FundamentalFilter

def test_fundamental_filter_pass():
    ff = FundamentalFilter("config/fundamental_rules.json")

    data = {
        "AAA": {
            "roe": 20,
            "roce": 18,
            "debt_to_equity": 0.2,
            "sales_growth_3y": 15,
            "profit_growth_3y": 15,
            "operating_cash_flow": 100
        }
    }

    result = ff.evaluate(data)
    assert result["AAA"]["approved"] is True
