from recommender.core import WorldState, CustomerProfile
from recommender import RecommenderService

def test_context_weather_hot():
    ws = WorldState.from_yaml("data/menu.yaml")
    ws.set_context("weather", "calor")
    svc = RecommenderService(ws)
    user = CustomerProfile()
    top = [d.id for _, d in svc.recommend(user, k=3)]
    assert any(x in top for x in ["gazpacho","ensalada_quinoa","bowl_frutas_yogur"])

def test_context_morning_breakfast():
    ws = WorldState.from_yaml("data/menu.yaml")
    ws.set_context("time_of_day", "mañana")
    svc = RecommenderService(ws)
    user = CustomerProfile()
    ids = [d.id for _, d in svc.recommend(user, k=5)]
    assert "huevos_rancheros" in ids or "bowl_frutas_yogur" in ids
