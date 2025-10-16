from typing import List
from .core import Dish, WorldState, CustomerProfile

def explain_score_components(dish: Dish, world: WorldState, user: CustomerProfile) -> List[str]:
    parts: List[str] = []
    if user.diets:
        missing = [d for d in user.diets if d not in dish.tags]
        if missing:
            parts.append("Penalización por dietas no compatibles: " + ", ".join(missing))
        else:
            parts.append("Compatible con dietas declaradas")
    al = [i for i in dish.ingredients if i in user.allergies]
    if al:
        parts.append("Contiene alérgenos: " + ", ".join(al))
    missing_ing = [i for i in dish.ingredients if not world.ingredients_availability.get(i, True)]
    if missing_ing:
        parts.append("Ingredientes faltantes: " + ", ".join(missing_ing))
    else:
        parts.append("Todos los ingredientes disponibles")
    hits_like = [t for t in (dish.ingredients + dish.tags + dish.name.lower().split()) if t in user.likes]
    if hits_like:
        parts.append("Coincide con gustos: " + ", ".join(sorted(set(hits_like))))
    hits_dislike = [t for t in (dish.ingredients + dish.tags + dish.name.lower().split()) if t in user.dislikes]
    if hits_dislike:
        parts.append("Coincide con disgustos: " + ", ".join(sorted(set(hits_dislike))))
    if world.context.get('time_of_day'):
        parts.append("Contexto hora del día: " + str(world.context['time_of_day']))
    if world.context.get('weather'):
        parts.append("Contexto clima: " + str(world.context['weather']))
    return parts
