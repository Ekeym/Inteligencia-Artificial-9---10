import streamlit as st
from typing import Dict
from kb import SEXOS, TIPO_TOS, DURACION_TOS, AUSCULTA, RECOMENDACIONES, DEFAULT_TRUE_CF
from engine import KnowledgeBase, InferenceEngine
from rules import RULES



st.set_page_config(page_title="SE Respiratorio", layout="wide")
st.title("Sistema Experto Respiratorio")


col1, col2, col3 = st.columns(3)
with col1:
    edad = st.number_input("Edad", min_value=0, max_value=110, value=40)
    sexo = st.selectbox("Sexo", SEXOS)
    tabaquismo = st.checkbox("Tabaquismo (≥10 pack-año)")
    exposicion = st.checkbox("Exposición a contaminantes")
    alergias = st.checkbox("Antecedentes alérgicos/atopia")


with col2:
    tos = st.selectbox("Tipo de tos", TIPO_TOS)
    dur_tos = st.selectbox("Duración de la tos", DURACION_TOS)
    disnea = st.checkbox("Disnea")
    sibilancias = st.checkbox("Sibilancias (sí)")
    dolor_toracico = st.checkbox("Dolor torácico")


with col3:
    fiebre = st.checkbox("Fiebre")
    fiebre_alta = st.checkbox("Fiebre > 38.5°C")
    ausc = st.selectbox("Auscultación", AUSCULTA)
    sat_baja = st.checkbox("Saturación O₂ < 92%")
    rx_consol = st.checkbox("Rx: consolidación")
    pcr_pos = st.checkbox("PCR SARS‑CoV‑2 positiva")
    uri_previa = st.checkbox("Infección respiratoria alta previa")
    contacto_caso = st.checkbox("Contacto con caso respiratorio viral")


st.markdown("---")

kb = KnowledgeBase()

if edad < 45:
    kb.assert_fact("edad_<45", 0.7)
else:
    kb.assert_fact("edad_>=45", 0.7)


if tabaquismo:
    kb.assert_fact("tabaquismo_importante", 0.7)


if exposicion:
    kb.assert_fact("exposicion_contaminantes", 0.7)


if alergias:
    kb.assert_fact("antecedente_atopia", 0.7)


# Síntomas
if tos != "ninguna":
    kb.assert_fact("tos_presente", 0.7)
if tos == "productiva":
    kb.assert_fact("tos_productiva", 0.7)
if tos in ("nocturna", "con_ejercicio"):
    kb.assert_fact("tos_nocturna_o_ejercicio", 0.7)


if dur_tos == ">=3sem":
    kb.assert_fact("duracion_tos_>=3sem", 0.7)
else:
    kb.assert_fact("duracion_tos_<3sem", 0.7)


if disnea:
    kb.assert_fact("disnea", 0.7)
if dur_tos != ">=3sem":
    kb.assert_fact("disnea_aguda", 0.7)
else:
    kb.assert_fact("disnea_cronica", 0.7)


if sibilancias:
    kb.assert_fact("sibilancias", 0.7)

if ausc == "crepitantes":
    kb.assert_fact("crepitantes", 0.7)
elif ausc == "roncus":
    kb.assert_fact("roncus", 0.6)
elif ausc == "sibilancias":
    kb.assert_fact("sibilancias", 0.7)

if sat_baja:
    kb.assert_fact("hipoxemia", 0.8)

if rx_consol:
    kb.assert_fact("rx_consolidacion", 0.85)
else:
    kb.assert_fact("rx_sin_consolidacion", 0.6)

if pcr_pos:
    kb.assert_fact("pcr_sarscov2_positiva", 0.95)

if uri_previa:
    kb.assert_fact("uri_previa", 0.7)

if contacto_caso:
    kb.assert_fact("contacto_caso", 0.7)


if sibilancias and (tos in ("nocturna", "con_ejercicio")):
    kb.assert_fact("variabilidad_sintomas", 0.6)


engine = InferenceEngine(RULES)
exp = engine.forward_chain(kb)


dx_labels = {
    "dx_asma": "Asma",
    "dx_neumonia": "Neumonía",
    "dx_bronquitis_aguda": "Bronquitis aguda",
    "dx_epoc": "EPOC",
    "dx_covid19": "COVID‑19",
}


resultados: Dict[str, float] = {k: v for k, v in kb.facts.items() if k.startswith("dx_")}
ordenados = sorted(resultados.items(), key=lambda kv: kv[1], reverse=True)


st.subheader("Resultados presuntivos (CF)")
if not ordenados:
    st.info("No hay suficiente evidencia para un diagnóstico presuntivo. Agregue datos.")
else:
    for clave, cf in ordenados:
        nombre = dx_labels.get(clave, clave)
        st.markdown(f"**{nombre}** — certeza **{cf:.0%}**")
        recs = RECOMENDACIONES.get(nombre.lower().replace(" ", ""), [])
        if recs:
            with st.expander("Recomendaciones de estudios (no terapéuticas)"):
                for r in recs:
                    st.write("- ", r)


st.subheader("¿Cómo se llegó a esta conclusión?")
if exp.trace:
    for line in exp.as_strings():
        st.code(line)
else:
    st.caption("Aún no se activó ninguna regla con la evidencia actual.")
