from src.core.recommendation_orchestrator import RecommendationOrchestrator


def main():
    print("Running Recommendation Engine...\n")

    orchestrator = RecommendationOrchestrator()
    buy_list = orchestrator.run()

    if not buy_list:
        print("No recommendations today.")
        return

    print("Top Recommendations:\n")

    for rec in buy_list:
        print(f"Symbol: {rec['symbol']}")
        print(f"Score: {rec['score']}")
        print(f"Buy Plan: {rec['buy_plan']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
