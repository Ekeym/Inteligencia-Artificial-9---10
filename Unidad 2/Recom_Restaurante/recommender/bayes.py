import math, random
from typing import Dict, Tuple
from .core import WorldState, CustomerProfile, Dish
from .persistence import dish_like_ratio

class BayesianScorer:
    def __init__(self,
                 w_prior: float = 1.0,
                 w_like: float = 1.0,
                 w_tag: float = 1.0,
                 unavail_penalty: float = -5.0,
                 allergy_penalty: float = -1e6,
                 dislike_penalty: float = -2.0,
                 w_feedback: float = 0.8,
                 epsilon: float = 0.02):
        self.w_prior = w_prior
        self.w_like = w_like
        self.w_tag = w_tag
        self.unavail_penalty = unavail_penalty
        self.allergy_penalty = allergy_penalty
        self.dislike_penalty = dislike_penalty
        self.w_feedback = w_feedback
        self.epsilon = epsilon

    def _logit(self, p: float) -> float:
        p = min(max(p, 1e-6), 1 - 1e-6)
        return math.log(p) - math.log(1 - p)

    def score_dish(self, dish: Dish, world: WorldState, user: CustomerProfile) -> float:
        score = 0.0
        score += self.w_prior * self._logit(dish.popularity)
        fr = dish_like_ratio(dish.id)
        if fr is not None:
            score += self.w_feedback * self._logit(fr)
        for diet in user.diets:
            if diet not in dish.tags:
                score += -20.0
        if any(ing in user.allergies for ing in dish.ingredients):
            return self.allergy_penalty
        if any(not world.ingredients_availability.get(ing, True) for ing in dish.ingredients):
            score += self.unavail_penalty
        for like in user.likes:
            if like in dish.ingredients or like in dish.tags or like in dish.name.lower():
                score += self.w_like * 1.0
        for dislike in user.dislikes:
            if dislike in dish.ingredients or dislike in dish.tags or dislike in dish.name.lower():
                score += self.dislike_penalty
        for t in dish.tags:
            if t in user.likes:
                score += self.w_tag * 0.5
        score += random.uniform(-self.epsilon, self.epsilon)
        return score

    def rank(self, world: WorldState, user: CustomerProfile) -> Dict[str, Tuple[float, Dish]]:
        scored = {d.id: (self.score_dish(d, world, user), d) for d in world.dishes.values()}
        return dict(sorted(scored.items(), key=lambda kv: kv[1][0], reverse=True))
