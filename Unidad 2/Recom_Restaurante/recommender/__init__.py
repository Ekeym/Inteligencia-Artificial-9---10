from .core import WorldState, CustomerProfile, Dish
from .bayes import BayesianScorer
from .rules import DefeasibleEngine, default_rules
from .explain import explain_score_components
from .persistence import init_db, add_feedback

class RecommenderService:
    def __init__(self, world: WorldState, scorer: BayesianScorer | None = None):
        self.world = world
        self.scorer = scorer or BayesianScorer()
        self.rules = DefeasibleEngine(default_rules())
        init_db()

    def recommend(self, user: CustomerProfile, k: int = 3):
        ranked = []
        for dish in self.world.dishes.values():
            base = self.scorer.score_dish(dish, self.world, user)
            final = self.rules.apply(base, self.world, user, dish)
            ranked.append((final, dish))
        ranked.sort(key=lambda x: x[0], reverse=True)
        return ranked[:k]

    def explain(self, user: CustomerProfile, dish: Dish):
        return explain_score_components(dish, self.world, user)

    def feedback(self, dish_id: str, like: bool, user_id: str | None = None):
        add_feedback(dish_id, like, user_id)
