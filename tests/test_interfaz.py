"""Pruebas de la portada y de la página del juego (sin navegador, con streamlit.testing)."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from core import juego_brecha as jb

RAIZ = Path(__file__).resolve().parent.parent


def test_html_del_juego_conserva_el_original_y_fija_mision_y_tema():
    html = jb.html_juego("m4", 3)
    original = jb.RUTA_HTML.read_text(encoding="utf-8")
    assert "window.__mision='m4'" in html
    assert "dataset.theme='papel'" in html and jb.PALETA_PAPEL in html
    # Fuera de las dos adaptaciones, el juego es el mismo archivo de la entrega.
    assert len(html) - len(original) - len(jb.PALETA_PAPEL) < 200
    with pytest.raises(ValueError):
        jb.html_juego("m9")


def test_portada_dispara_la_entrada_desde_el_ladron():
    carpeta = RAIZ / "ui" / "portada"
    html = (carpeta / "escena.html").read_text(encoding="utf-8")
    js = (carpeta / "interaccion.js").read_text(encoding="utf-8")
    assert 'id="ladron"' in html and 'role="button"' in html
    assert 'setTriggerValue("entrar", true)' in js
    # Sin recursos externos: funciona igual en local y en Streamlit Cloud.
    assert "http" not in html and "http" not in js


def _app(pagina: str | None = None) -> AppTest:
    """Corre app.py (con su navegación) y, si se indica, cambia a una página."""
    at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=60).run()
    if pagina:
        at.switch_page(pagina).run()
    return at


@pytest.mark.parametrize("pagina", [None, "vistas/inicio.py", "vistas/juego.py"])
def test_paginas_sin_excepciones(pagina):
    assert not _app(pagina).exception


def test_cuestionario_del_juego_valida_con_la_logica_del_juego():
    at = _app("vistas/juego.py")
    at.radio(key="quiz_0").set_value(str(jb.mejor_combinacion()["n_señales"])).run()
    at.radio(key="quiz_3").set_value("No").run()
    assert not at.exception
    assert sum("Correcto" in s.value for s in at.success) == 2


def test_pagina_astar_conserva_la_logica_en_cada_ciudad_y_paso():
    from core import busqueda as bq
    at = _app("vistas/logistica.py")
    for ciudad in bq.CIUDADES:
        at.button_group[0].set_value(ciudad).run()
        destino = at.selectbox[0].value
        esperado = bq.a_estrella(ciudad, destino)
        slider = at.slider[0]
        assert slider.max == len(esperado.expandidos)
        for paso in range(1, int(slider.max) + 1):
            slider.set_value(paso).run()
            assert not at.exception
        html = "".join(h.proto.body for h in at.get("html"))
        assert all(n in html for n in esperado.camino)
