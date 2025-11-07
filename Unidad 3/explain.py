from dataclasses import dataclass
from typing import List


@dataclass
class FiredRule:
    name: str
    antecedents: List[str]
    cf_antecedent: float
    conclusion: str
    cf_rule: float
    cf_result: float


class Explanation:
    def __init__(self):
        self.trace: List[FiredRule] = []

    def add(self, fired: FiredRule):
        self.trace.append(fired)

    def as_strings(self) -> List[str]:
        lines = []
        
        for fr in self.trace:

            antecedentes_texto = ", ".join(
                a.replace("_", " ").capitalize() for a in fr.antecedents
            )
            conclusion_texto = fr.conclusion.replace("_", " ").capitalize()

            texto = (
                f"Se activó la regla \"{fr.name}\" porque se detectaron: {antecedentes_texto}. "
                f"Esto sugiere {conclusion_texto.lower()} con una certeza aproximada del "
                f"{fr.cf_result * 100:.0f}%. "
                f"(Confianza de la regla: {fr.cf_rule * 100:.0f}%, fuerza de la evidencia: {fr.cf_antecedent * 100:.0f}%)."
            )
            lines.append(texto)
        return lines
