from dataclasses import dataclass
from typing import Callable, List
from .core import WorldState, CustomerProfile, Dish

@dataclass
class Rule:
    name: str
    priority: int
    applies: Callable[[WorldState, CustomerProfile, Dish], bool]
    effect: Callable[[float], float]

class DefeasibleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = sorted(rules, key=lambda r: -r.priority)

    def apply(self, base_score: float, world: WorldState, user: CustomerProfile, dish: Dish) -> float:
        score = base_score
        for r in self.rules:
            if r.applies(world, user, dish):
                score = r.effect(score)
        return score

def default_rules() -> List[Rule]:
    return [
        Rule(
            name="ban_allergy",
            priority=100,
            applies=lambda w,u,d: any(ing in u.allergies for ing in d.ingredients),
            effect=lambda s: -1e9,
        ),
        Rule(
            name="defeat_seafood_for_vegans",
            priority=80,
            applies=lambda w,u,d: ("vegano" in u.diets) and any(x in d.ingredients for x in ["salmon", "atun", "marisco"]),
            effect=lambda s: s - 50.0,
        ),
        Rule(
            name="boost_fully_available",
            priority=60,
            applies=lambda w,u,d: all(w.ingredients_availability.get(ing, True) for ing in d.ingredients),
            effect=lambda s: s + 1.0,
        ),
        Rule(
            name="weather_hot_prefers_cold_light",
            priority=50,
            applies=lambda w,u,d: w.context.get('weather') == 'calor' and any(t in d.tags for t in ['frio','ligero']),
            effect=lambda s: s + 1.5,
        ),
        Rule(
            name="weather_cold_prefers_hot",
            priority=50,
            applies=lambda w,u,d: w.context.get('weather') == 'frio' and 'caliente' in d.tags,
            effect=lambda s: s + 1.5,
        ),
        Rule(
            name="morning_prefers_breakfast",
            priority=50,
            applies=lambda w,u,d: w.context.get('time_of_day') == 'mañana' and 'desayuno' in d.tags,
            effect=lambda s: s + 1.5,
        ),
        Rule(
            name="night_discourage_spicy_if_dislike",
            priority=40,
            applies=lambda w,u,d: (w.context.get('time_of_day') == 'noche') and ('picante' in d.tags) and ('picante' in u.dislikes),
            effect=lambda s: s - 2.0,
        ),
    ]
