"""Punto de entrada de la aplicación Streamlit: configuración y navegación."""
import streamlit as st

from ui import estado
from ui.componentes import CSS_PORTADA, aplicar_estilos

REPOSITORIO = "https://github.com/mapsita123/TrabajoIA"
APP_PUBLICADA = "https://nequi-ia-app-un3zhq5ntx3nx4cff94ksn.streamlit.app/"

st.set_page_config(page_title="Nequi IA · Fundamentos de IA", page_icon="🛡️", layout="wide")
aplicar_estilos()
estado.init()

portada = st.Page("vistas/portada.py", title="Portada", icon=":material/theater_comedy:", default=True)
paginas = {
    "": [
        portada,
        st.Page("vistas/inicio.py", title="Inicio", icon=":material/home:", url_path="inicio"),
        st.Page("vistas/evaluar.py", title="Evaluar una solicitud", icon=":material/fact_check:"),
    ],
    "Componentes por sprint": [
        st.Page("vistas/logistica.py", title="1 · Logística (A*)", icon=":material/route:"),
        st.Page("vistas/sistema_experto.py", title="2 · Sistema experto", icon=":material/rule:"),
        st.Page("vistas/evolutivo.py", title="3 · Estrategia evolutiva", icon=":material/genetics:"),
        st.Page("vistas/juegos.py", title="3 · Teoría de juegos", icon=":material/swords:"),
        st.Page("vistas/juego.py", title="3 · Juego Brecha Nequi", icon=":material/sports_esports:"),
        st.Page("vistas/difuso.py", title="4 · Lógica difusa", icon=":material/blur_on:"),
    ],
    "Calidad": [
        st.Page("vistas/validacion.py", title="Validación y pruebas", icon=":material/verified:"),
    ],
}

pagina = st.navigation(paginas)
if pagina.url_path == portada.url_path:
    st.html(CSS_PORTADA)
else:
    with st.sidebar:
        c1, c2 = st.columns(2)
        c1.link_button("GitHub", REPOSITORIO, icon=":material/code:", width="stretch")
        c2.link_button("App", APP_PUBLICADA, icon=":material/open_in_new:", width="stretch")
        st.caption("Fundamentos de IA · Universidad EIA · 2026-2\n\n"
                   "Caso académico simulado. No usa datos ni sistemas reales de Nequi.")
pagina.run()
