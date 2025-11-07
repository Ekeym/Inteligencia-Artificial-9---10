from typing import Dict, List

SEXOS = ["F", "M", "Otro"]
TIPO_TOS = ["ninguna", "seca", "productiva", "nocturna", "con_ejercicio"]
DURACION_TOS = ["<3d", "3-7d", ">7d", ">=3sem"]
AUSCULTA = ["normal", "sibilancias", "crepitantes", "roncus"]

RECOMENDACIONES: Dict[str, List[str]] = {
"asma": [
    "Espirometría con prueba broncodilatadora",
    "Peak flow seriado (variabilidad)",
    "Pruebas de alergia si procede"
],
"neumonia": [
    "Radiografía/US pulmonar",
    "Hemograma, PCR/procalcitonina",
    "Oximetría y gasometría si hipoxemia"
],
"bronquitis_aguda": [
    "Evaluación clínica; Rx solo si signos de consolidación",
    "Descartar neumonía si fiebre alta o hipoxemia"
],
"epoc": [
    "Espirometría (FEV1/FVC < 0.70)",
    "Oximetría de pulso y evaluación de exacerbaciones"
],
"covid19": [
    "Prueba de antígeno/PCR",
    "Oximetría de pulso",
    "Imagen si disnea o saturación baja"
],
}

DEFAULT_TRUE_CF = 0.7
DEFAULT_FALSE_CF = 0.0