from dataclasses import dataclass, field
from typing import List, Dict, Any
import yaml
from pathlib import Path

@dataclass
class Dish:
    id: str
    name: str
    ingredients: List[str]
    tags: List[str]
    popularity: float = 0.5

@dataclass
class WorldState:
    ingredients_availability: Dict[str, bool]
    dishes: Dict[str, Dish]
    context: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "WorldState":
        data = yaml.safe_load(Path(path).read_text())
        dishes = {
            d["id"]: Dish(
                id=d["id"],
                name=d["name"],
                ingredients=d.get("ingredients", []),
                tags=d.get("tags", []),
                popularity=float(d.get("popularity", 0.5)),
            )
            for d in data.get("dishes", [])
        }
        availability = {k: bool(v.get("available", True)) for k, v in data.get("ingredients", {}).items()}
        return cls(ingredients_availability=availability, dishes=dishes, context={})

    def set_availability(self, ingredient: str, available: bool) -> None:
        self.ingredients_availability[ingredient] = available

    def set_context(self, key: str, value: Any) -> None:
        self.context[key] = value

@dataclass
class CustomerProfile:
    likes: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)
    diets: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    user_id: str | None = None
