"""
Portada interactiva (componente de Streamlit v2 con HTML, CSS y JS propios).

La escena, los estilos y la interacción viven en archivos separados de esta
carpeta. Todo es inline: no carga imágenes ni scripts externos, así que
funciona igual en local y en Streamlit Community Cloud.
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v2  # noqa: F401  (registra st.components.v2)

_CARPETA = Path(__file__).resolve().parent

_portada = st.components.v2.component(
    "portada_ladron",
    html=(_CARPETA / "escena.html").read_text(encoding="utf-8"),
    css=(_CARPETA / "estilo.css").read_text(encoding="utf-8"),
    js=(_CARPETA / "interaccion.js").read_text(encoding="utf-8"),
)


def portada() -> bool:
    """Monta la portada y devuelve True en la ejecución en que el usuario atrapa al ladrón."""
    resultado = _portada(key="portada_ladron", on_entrar_change=lambda: None)
    return bool(resultado.entrar)
