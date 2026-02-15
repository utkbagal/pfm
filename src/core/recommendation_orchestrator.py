from typing import List, Dict

from src.data_layer.universe_loader import StockUniverseLoader
from src.data_layer.market_data_loader import MarketDataLoader
from src.data_layer.indicator_engine import IndicatorEngine

from src.intelligence.fundamental_filter import FundamentalFilter
from src.intelligence.liquidity_volatility_filter import LiquidityVolatilityFilter
from src.intelligence.market_regime_analyzer import MarketRegimeAnalyzer
from src.intelligence.sector_strength_analyzer import SectorStrengthAnalyzer

from src.setups.trend_analyzer import TrendAnalyzer
from src.setups.setup_engine import SetupDetectionEngine

from src.decision.eligibility_engine import EligibilityEngine
from src.decision.scoring_engine import ScoringEngine
from src.decision.buy_plan_generator import BuyPlanGenerator
from src.decision.evidence_builder import EvidenceBuilder

from src.persistence.recommendation_logger import RecommendationLogger


class RecommendationOrchestrator:

    def __init__(self):
        # Data
        self.universe_loader = StockUniverseLoader("config/universe.csv")
        self.market_loader = MarketDataLoader("config/market_data.json")
        self.indicator_engine = IndicatorEngine()

        # Intelligence
        self.fundamental_filter = FundamentalFilter("config/fundamental_rules.json")
        self.liquidity_filter = LiquidityVolatilityFilter("config/liquidity_rules.json")
        self.market_regime = MarketRegimeAnalyzer("config/market_regime_rules.json")
        self.sector_analyzer = SectorStrengthAnalyzer("config/sector_strength_rules.json")

        # Setups
        self.trend_analyzer = TrendAnalyzer("config/trend_rules.json")
        self.setup_engine = SetupDetectionEngine()

        # Decision
        self.eligibility_engine = EligibilityEngine("config/eligibility_rules.json")
        self.scoring_engine = ScoringEngine("config/scoring_weights.json")
        self.buy_plan_generator = BuyPlanGenerator()
        self.evidence_builder = EvidenceBuilder()

        # Persistence
        self.logger = RecommendationLogger()

    # ---------------------------------------------------

    def run(self) -> List[Dict]:

        recommendations = []

        # 1️⃣ Load universe
        universe = self.universe_loader.load()
        symbols = universe.symbols

        # 2️⃣ Fetch market + stock data
        ohlcv_data = self.market_loader.fetch(symbols)

        # 3️⃣ Compute indicators
        indicator_data = self.indicator_engine.compute(ohlcv_data)

        # 4️⃣ Market regime (use index symbol separately in production)
        # For now assume NIFTY included in config
        # Example placeholder:
        # market_state = self.market_regime.analyze(index_df)
        market_state = {"regime": "BULLISH"}

        # 5️⃣ Loop per stock
        for symbol in symbols:

            df = indicator_data.get(symbol)
            if df is None:
                continue

            # Placeholder fundamental & sector data (to integrate properly later)
            fundamental_status = {"approved": True}
            liquidity_status = self.liquidity_filter.evaluate({symbol: df})[symbol]
            sector_status = {"strength": "STRONG"}  # integrate properly later

            trend_info = self.trend_analyzer.analyze(df)
            setups = self.setup_engine.detect_setups(df, trend_info)

            context = {
                "symbol": symbol,
                "fundamental": fundamental_status,
                "liquidity": liquidity_status,
                "market_regime": market_state,
                "sector_strength": sector_status,
                "trend": trend_info,
                "setups": setups,
                "position_state": "NO_POSITION"
            }

            eligibility = self.eligibility_engine.evaluate(context)

            if not eligibility["eligible"]:
                continue

            score_result = self.scoring_engine.score(context)

            context["score"] = score_result

            buy_plan = self.buy_plan_generator.generate({
                "indicator_df": df,
                "setups": setups,
                "trend": trend_info
            })

            context["buy_plan"] = buy_plan

            evidence = self.evidence_builder.build(context)

            self.logger.log(evidence)

            recommendations.append({
                "symbol": symbol,
                "score": score_result["score"],
                "buy_plan": buy_plan
            })

        # 6️⃣ Sort by score
        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return recommendations
