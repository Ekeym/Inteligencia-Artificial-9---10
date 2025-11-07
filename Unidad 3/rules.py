from typing import List, Dict, Any


Rule = Dict[str, Any]


RULES: List[Rule] = [
# ASMA
{
    "name": "asma_sibilancias_nocturna_atopia",
    "if_all": ["sibilancias", "tos_nocturna_o_ejercicio", "antecedente_atopia"],
    "then": ("dx_asma", 0.90),
},
{
    "name": "asma_joven_var_wheeze",
    "if_all": ["sibilancias", "edad_<45", "variabilidad_sintomas"],
    "then": ("dx_asma", 0.75),
},


# NEUMONÍA
{
    "name": "neumonia_fiebre_crepitantes_dispnea_tos_prod",
    "if_all": ["fiebre_alta", "crepitantes", "disnea_aguda", "tos_productiva"],
    "then": ("dx_neumonia", 0.85),
},
{
    "name": "neumonia_rx_consolidacion",
    "if_all": ["rx_consolidacion"],
    "then": ("dx_neumonia", 0.80),
},


# BRONQUITIS AGUDA
{
    "name": "bronquitis_tos_<3sem_uri_prev_sin_rx",
    "if_all": ["tos_presente", "duracion_tos_<3sem", "uri_previa", "rx_sin_consolidacion"],
    "then": ("dx_bronquitis_aguda", 0.75),
},


# EPOC
{
    "name": "epoc_tabaquismo_cronica_disnea",
    "if_all": ["tabaquismo_importante", "tos_cronica", "disnea_cronica", "edad_>=45"],
    "then": ("dx_epoc", 0.80),
},


# COVID-19 (genérica)
{
    "name": "covid_fiebre_tos_disnea_contacto",
    "if_all": ["fiebre", "tos_presente", "disnea", "contacto_caso"],
    "then": ("dx_covid19", 0.80),
},
{
    "name": "covid_pcr_positiva",
    "if_all": ["pcr_sarscov2_positiva"],
    "then": ("dx_covid19", 0.95),
},
]