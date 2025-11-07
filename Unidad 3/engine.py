from typing import Dict, List, Tuple
from explain import Explanation, FiredRule


def cf_and(values: List[float]) -> float:
    return min(values) if values else 0.0


def cf_or(values: List[float]) -> float:
    return max(values) if values else 0.0


def combine_cf(cf_old: float, cf_new: float) -> float:
    if cf_old == 0:
        return cf_new
    if cf_old > 0 and cf_new > 0:
        return cf_old + (1 - cf_old) * cf_new
    if cf_old < 0 and cf_new < 0:
        return cf_old + (1 + cf_old) * cf_new
    denom = 1 - min(abs(cf_old), abs(cf_new))
    if denom == 0:
        return 0.0
    return (cf_old + cf_new) / denom


class KnowledgeBase:
    def __init__(self):
        self.facts: Dict[str, float] = {}


    def assert_fact(self, fact: str, cf: float):
        old = self.facts.get(fact, 0.0)
        self.facts[fact] = combine_cf(old, cf)


    def get(self, fact: str) -> float:
        return self.facts.get(fact, 0.0)


class InferenceEngine:
    def __init__(self, rules: List[dict]):
        self.rules = rules


    def forward_chain(self, kb: KnowledgeBase) -> Explanation:
        exp = Explanation()
        changed = True
        applied = set()
        while changed:
            changed = False
            for r in self.rules:
                name = r["name"]
                if name in applied:
                    continue
                antecedents = r.get("if_all", [])
                cfs = [kb.get(a) for a in antecedents]
                if all(cf != 0 for cf in cfs):
                    cf_ant = cf_and(cfs)
                    concl, cf_rule = r["then"]
                    cf_res = cf_ant * cf_rule
                    before = kb.get(concl)
                    kb.assert_fact(concl, cf_res)
                    after = kb.get(concl)
                    if abs(after - before) > 1e-6:
                        changed = True
                        applied.add(name)
                        exp.add(FiredRule(name, antecedents, cf_ant, concl, cf_rule, cf_res))
        return exp


    def backward_chain(self, kb: KnowledgeBase, goal: str) -> Tuple[float, Explanation]:
        exp = Explanation()
        relevant = [r for r in self.rules if r["then"][0] == goal]
        cfs_goal: List[float] = []

        for r in relevant:
            antecedents = r.get("if_all", [])
            cfs_ant = [kb.get(a) for a in antecedents]

            if all(cf != 0 for cf in cfs_ant):
                cf_ant = cf_and(cfs_ant)
                cf_rule = r["then"][1]
                cf_res = cf_ant * cf_rule
                cfs_goal.append(cf_res)
                exp.add(FiredRule(r["name"], antecedents, cf_ant, goal, cf_rule, cf_res))
                
        return (cf_or(cfs_goal) if cfs_goal else 0.0, exp)