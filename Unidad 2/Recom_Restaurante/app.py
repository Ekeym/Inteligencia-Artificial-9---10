
import streamlit as st
from recommender.core import WorldState, CustomerProfile
from recommender import RecommenderService
from recommender.persistence import global_like_ratios
from typing import List

st.set_page_config(page_title="Recomendador de Menú", page_icon="🍽️", layout="wide")

try:
    with open("assets/styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.info("No se encontró assets/styles.css; corriendo con estilo por defecto.")


st.markdown("### Recomendador de Menú **")

if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "last_params" not in st.session_state:
    st.session_state.last_params = None

ws = WorldState.from_yaml("data/menu.yaml")
service = RecommenderService(ws)

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    with st.container():
        st.markdown('<div class="kpi"><div>Platos</div><h3>' + str(len(ws.dishes)) + "</h3></div>", unsafe_allow_html=True)
with kpi2:
    with st.container():
        st.markdown('<div class="kpi"><div>Ingredientes</div><h3>' + str(len(ws.ingredients_availability)) + "</h3></div>", unsafe_allow_html=True)
with kpi3:
    with st.container():
        ratios = global_like_ratios()
        coverage = f"{len(ratios)} con feedback" if ratios else "0 con feedback"
        st.markdown(f'<div class="kpi"><div>Feedback</div><h3>{coverage}</h3></div>', unsafe_allow_html=True)

st.markdown('<hr class="soft" />', unsafe_allow_html=True)

tab_rec, tab_ing, tab_stats = st.tabs(["Recomendar", "Ingredientes", "Métricas"])

with tab_ing:
    st.subheader("Disponibilidad de ingredientes")
    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        if st.button("Seleccionar todos"):
            for k in list(ws.ingredients_availability.keys()):
                ws.ingredients_availability[k] = True
                st.session_state[f"ing_{k}"] = True
    with c2:
        if st.button("Limpiar todos"):
            for k in list(ws.ingredients_availability.keys()):
                ws.ingredients_availability[k] = False
                st.session_state[f"ing_{k}"] = False

    st.write("")
    cols = st.columns(3)
    keys = list(ws.ingredients_availability.keys())
    for i, ing in enumerate(keys):
        with cols[i % 3]:
            ws.ingredients_availability[ing] = st.toggle(ing, value=ws.ingredients_availability[ing], key=f"ing_{ing}")

with tab_stats:
    st.subheader("Métricas de likes aprendidas")
    ratios = global_like_ratios()
    if not ratios:
        st.info("Aún no hay feedback registrado. Usa los botones 👍/👎 en las recomendaciones.")
    else:
        for dish_id, r in sorted(ratios.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"- **{dish_id}** → {r:.2f}")

with tab_rec:
    left, right = st.columns([0.95, 1.05])

    with left:
        st.subheader("Perfil del cliente")
        with st.expander("Presets rápidos", expanded=False):
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("Vegano fresco"):
                st.session_state["likes"] = ["vegano","frio","ligero"]
                st.session_state["diets"] = ["vegano"]
                st.session_state["dislikes"] = []
            if c2.button("Desayuno suave"):
                st.session_state["likes"] = ["desayuno","ligero","frio"]
                st.session_state["diets"] = []
                st.session_state["dislikes"] = ["picante"]
            if c3.button("Carne & caliente"):
                st.session_state["likes"] = ["pollo","caliente"]
                st.session_state["diets"] = []
                st.session_state["dislikes"] = []
            if c4.button("Picante lovers"):
                st.session_state["likes"] = ["picante"]
                st.session_state["diets"] = []
                st.session_state["dislikes"] = []

        user_id = st.text_input("ID de usuario (opcional, para aprendizaje)", value="")

        likes = st.multiselect(
            "Gustos (ingredientes/etiquetas/palabras)",
            ["picante","pollo","mozzarella","quinoa","curry","salmon","vegano","sin_gluten","vegetariano","desayuno","frio","ligero","caliente"],
            default=st.session_state.get("likes", []),
            key="likes"
        )
        dislikes = st.multiselect(
            "Disgustos",
            ["picante","mozzarella","ajo","curry","salmon"],
            default=st.session_state.get("dislikes", []),
            key="dislikes"
        )
        diets = st.multiselect(
            "Dietas",
            ["vegano","vegetariano","sin_gluten"],
            default=st.session_state.get("diets", []),
            key="diets"
        )
        allergies = st.multiselect(
            "Alergias (ingredientes)",
            list(ws.ingredients_availability.keys()),
            default=st.session_state.get("allergies", []),
            key="allergies"
        )

        st.subheader("Contexto")
        tc1, tc2 = st.columns(2)
        with tc1:
            time_of_day = st.selectbox("Hora del día", ["mañana","tarde","noche"], index=1, key="time_of_day")
        with tc2:
            weather = st.selectbox("Clima", ["templado","calor","frio"], index=0, key="weather")
        ws.set_context("time_of_day", time_of_day)
        ws.set_context("weather", weather)

        k = st.slider("¿Cuántas recomendaciones?", 1, 6, 4)

        st.subheader("Filtros de resultado")
        cf1, cf2, cf3 = st.columns([1,1,1])
        with cf1:
            q = st.text_input("Buscar por nombre", value="")
        with cf2:
            filter_tag = st.selectbox("Filtrar por etiqueta", ["(ninguno)","vegano","vegetariano","sin_gluten","picante","frio","caliente","ligero","desayuno"])
        with cf3:
            min_pop = st.slider("Popularidad mínima", 0.0, 1.0, 0.0, 0.05)

        do_recommend = st.button("Obtener recomendaciones", use_container_width=True)
        if do_recommend:
            st.session_state.show_results = True
            st.session_state.last_params = {
                "user_id": user_id,
                "likes": likes, "dislikes": dislikes, "diets": diets, "allergies": allergies,
                "time_of_day": time_of_day, "weather": weather,
                "q": q, "filter_tag": filter_tag, "min_pop": min_pop, "k": k,
            }

with right:
    st.subheader("Resultados")

    params = None
    if st.session_state.show_results and st.session_state.last_params is not None:
        params = st.session_state.last_params
    else:
        params = {
            "user_id": user_id,
            "likes": likes, "dislikes": dislikes, "diets": diets, "allergies": allergies,
            "time_of_day": time_of_day, "weather": weather,
            "q": q, "filter_tag": filter_tag, "min_pop": min_pop, "k": k,
        }

    ws.set_context("time_of_day", params["time_of_day"])
    ws.set_context("weather", params["weather"])

    user = CustomerProfile(
        likes=params["likes"],
        dislikes=params["dislikes"],
        diets=params["diets"],
        allergies=params["allergies"],
        user_id=(params["user_id"] or None),
    )

    if st.session_state.show_results:
        results = service.recommend(user, k=params["k"])

        # Filtros
        filtered = []
        for score, dish in results:
            if params["q"] and params["q"].lower() not in dish.name.lower():
                continue
            if params["filter_tag"] != "(ninguno)" and params["filter_tag"] not in dish.tags:
                continue
            if dish.popularity < params["min_pop"]:
                continue
            filtered.append((score, dish))

        if not filtered:
            st.warning("No hay resultados con los filtros actuales.")
        else:
            for score, dish in filtered:
                tags_html = " ".join([f'<span class="badge tag-{t}">{t}</span>' for t in dish.tags])
                card = f'''
                <div class="card">
                  <h3>{dish.name}</h3>
                  <div class="smallmuted">Score: {score:.2f} · Popularidad: {dish.popularity:.2f}</div>
                  <div style="margin:0.4rem 0;">{tags_html}</div>
                  <div class="smallmuted">Ingredientes: {", ".join(dish.ingredients)}</div>
                </div>
                '''
                st.markdown(card, unsafe_allow_html=True)

                with st.expander("¿Por qué se recomendó este plato?"):
                    for line in service.explain(user, dish):
                        st.write("• " + line)

                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"Me gusta ({dish.id})", key=f"like_{dish.id}"):
                        service.feedback(dish.id, True, user.user_id)
                        st.session_state.show_results = True
                        st.toast("Registrado 👍")
                        st.rerun()

                with c2:
                    if st.button(f"No me gusta ({dish.id})", key=f"dislike_{dish.id}"):
                        service.feedback(dish.id, False, user.user_id)
                        st.session_state.show_results = True
                        st.toast("Registrado 👎")
                        st.rerun()

