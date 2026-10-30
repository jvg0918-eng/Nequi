import streamlit as st

from ui.portada import portada

# El clic sobre el ladrón dispara «entrar»: se marca la llegada (para el telón
# de inicio) y se cambia a la página principal.
if portada():
    st.session_state["llegada_desde_portada"] = True
    st.switch_page("vistas/inicio.py")
