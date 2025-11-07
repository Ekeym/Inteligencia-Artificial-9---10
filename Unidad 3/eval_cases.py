from typing import List, Dict
from engine import KnowledgeBase, InferenceEngine
from rules import RULES


CASES: List[Dict] = [
{
    "name": "Neumonía clásica",
    "facts": {
        "fiebre_alta": 0.8, "crepitantes": 0.7, "disnea_aguda": 0.7, "tos_productiva": 0.7
    },
    "gold": "dx_neumonia",
},
{
    "name": "Asma típica",
    "facts": {
        "sibilancias": 0.7, "tos_nocturna_o_ejercicio": 0.7, "antecedente_atopia": 0.7
    },
    "gold": "dx_asma",
},
{
    "name": "Bronquitis aguda",
    "facts": {
        "tos_presente": 0.7, "duracion_tos_<3sem": 0.7, "uri_previa": 0.7, "rx_sin_consolidacion": 0.6
    },
    "gold": "dx_bronquitis_aguda",
},
]


def run_eval(threshold: float = 0.5):
    engine = InferenceEngine(RULES)
    tp = tn = fp = fn = 0
    for c in CASES:
        kb = KnowledgeBase()
        for f, v in c["facts"].items():
            kb.assert_fact(f, v)
        exp = engine.forward_chain(kb)
        pred_cf = kb.facts.get(c["gold"], 0.0)
        pred = pred_cf >= threshold
        if pred:
            tp += 1
        else:
            fn += 1
        precision = tp / (tp + fp) if (tp + fp) else 0
        sensibilidad = tp / (tp + fn) if (tp + fn) else 0
        especificidad = tn / (tn + fp) if (tn + fp) else 0
    print(f"Sensibilidad: {sensibilidad:.2f} | Especificidad: {especificidad:.2f} | Precisión: {precision:.2f}")


if __name__ == "__main__":
    run_eval()