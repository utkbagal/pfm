from src.data_layer.universe_loader import StockUniverseLoader

def test_universe_csv_load():
    loader = StockUniverseLoader("config/universe.csv")
    universe = loader.load()

    assert len(universe.stocks) > 0
    assert "RELIANCE" in universe.symbols
