"""Piezas de interfaz compartidas: estilos, etiquetas de decisión y gráficos."""
from __future__ import annotations

import re

import numpy as np
import plotly.graph_objects as go
import streamlit as st

COLOR_PRIMARIO = "#C8322A"   # rojo del hilo de la ilustración (assets/ladron_tinta.jpg) y del tema
COLOR_SECUNDARIO = "#1B1A17"  # tinta negra del mismo dibujo
TINTA, PAPEL, ROJO = "#1B1A17", "#F1EAD9", "#C8322A"
PAPEL_CLARO, PAPEL_OSCURO = "#F7F2E6", "#E8DFCA"
AZUL, ORO, VERDE, GRIS = "#2B5C9E", "#B07A10", "#2F7D4F", "#8A7F6C"

# Guía cromática: cada tono tiene un color de trazo (texto, bordes, acentos) y un fondo suave.
# Todos los trazos cumplen contraste ≥ 4.5:1 sobre su fondo y sobre el papel.
TONOS = {
    "rojo": ("#C8322A", "#F6DCD5"),
    "azul": ("#2B5C9E", "#DCE5F1"),
    "oro": ("#946508", "#F3E6C4"),
    "verde": ("#2F7D4F", "#DBE9DD"),
    "tinta": ("#1B1A17", "#E8DFCA"),
}
# Un tono por módulo: así cada sección se reconoce por su color en el menú, el inicio y su página.
TONO_MODULO = {"logistica": "azul", "sistema_experto": "rojo", "evolutivo": "oro", "juegos": "tinta",
               "juego": "rojo", "difuso": "verde", "evaluar": "rojo", "validacion": "verde"}

COLORES_ETIQUETA = {"bajo": "#2F7D4F", "medio": "#B07A10", "alto": "#C8322A",
                    "holgada": "#2F7D4F", "moderada": "#B07A10", "excedida": "#C8322A",
                    "aceptable": "#2F7D4F", "excesivo": "#C8322A"}

DECISIONES = {
    "APROBADO": ("Aprobado", "ok"),
    "REVISION_MANUAL": ("Revisión manual", "warn"),
    "RECHAZADO_POR_FRAUDE": ("Rechazado por fraude", "bad"),
    "RECHAZADO_POR_RIESGO_FINANCIERO": ("Rechazado por riesgo financiero", "bad"),
    "ALERTA_DE_RIESGO": ("Alerta de riesgo", "bad"),
    "SIN_ALERTA_DEL_MODELO": ("Sin alerta", "ok"),
    "REQUIERE_VERIFICACION_BIOMETRICA": ("Requiere verificación biométrica", "bad"),
}

_MANO = "255px 14px 225px 14px / 14px 225px 14px 255px"   # esquinas irregulares de trazo a mano


def _css_tonos() -> str:
    """Tarjetas por tono: st.container(key="t_<tono>_...") recibe fondo, borde y sombra de su color."""
    reglas = []
    for nombre, (trazo, fondo) in TONOS.items():
        k = f'[class*="st-key-t_{nombre}"]'
        reglas.append(f"{k} {{background: {fondo}; border: 1.6px solid {trazo} !important; border-radius: {_MANO} !important;"
                      f" box-shadow: 4px 4px 0 {trazo}; padding: 1rem 1.1rem !important;}}")
        reglas.append(f"{k} [data-testid=\"stMetric\"] {{background: transparent; border: none; box-shadow: none; padding: 0;}}")
        reglas.append(f"{k} [data-testid=\"stMetricValue\"], {k} .ceja, {k} .paso {{color: {trazo};}}")
        reglas.append(f".chip.t-{nombre} {{color: {trazo}; border-color: {trazo}; background: {fondo};}}")
    return "\n".join(reglas)


CSS = """
<style>
@import url("https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&display=swap");
.block-container {padding-top: 3.2rem; max-width: 1240px;}
h1 {letter-spacing: -.01em;}

/* ---------- jerarquía: ceja de color, título, trazo y bajada ---------- */
.paso, .ceja {font: 600 .74rem "IBM Plex Mono", monospace; color: var(--t, #C8322A); text-transform: uppercase; letter-spacing: .14em;}
.ceja {margin-bottom: .35rem;}
.trazo {display: block; width: 150px; height: 14px; margin: -.55rem 0 .7rem;}
.bajada {color: #3d3830; font-size: 1.08rem; max-width: 50em; margin-top: -.2rem;}
.num {font: 700 1.35rem "Caveat", cursive; color: #C8322A; letter-spacing: .02em;}
.nota {font: 600 1.35rem "Caveat", cursive; color: #C8322A;}
.seccion {display: flex; align-items: center; gap: .8rem; margin: 1.6rem 0 .4rem;}
.seccion .insignia {flex: 0 0 auto; display: grid; place-items: center; width: 2.4rem; height: 2.4rem; border-radius: 50%;
  background: var(--t); color: #fff; font: 700 1.25rem "Caveat", cursive; box-shadow: 2px 2px 0 #1B1A17;}
.seccion h2 {margin: 0; padding: 0; font: 600 1.55rem "Fraunces", Georgia, serif; color: #1B1A17; line-height: 1.15;}
.seccion p {margin: .1rem 0 0; color: #4a453d; font-size: .95rem;}

/* ---------- tarjetas y bloques a mano ---------- */
[data-testid="stExpander"] details, .dec {border: 1.6px solid #2b2824 !important; border-radius: """ + _MANO + """ !important;}
[data-testid="stExpander"] details {background: #F7F2E6;}
[data-testid="stExpander"] summary {background: #E8DFCA; font-weight: 600;}
.dec {padding: 14px 18px; margin: 4px 0 12px 0; background: #F7F2E6;}
.dec .lbl {font: 600 .74rem "IBM Plex Mono", monospace; text-transform: uppercase; letter-spacing: .1em; opacity: .75;}
.dec .val {font: 650 1.5rem "Fraunces", Georgia, serif; margin-top: 2px;}
.dec .why {font-size: .92rem; margin-top: 4px;}
.dec.ok   {background: #DBE9DD; border-color: #2F7D4F !important; box-shadow: 4px 4px 0 #2F7D4F;}
.dec.ok .val {color: #2F7D4F;}
.dec.warn {background: #F3E6C4; border-color: #946508 !important; box-shadow: 4px 4px 0 #946508;}
.dec.warn .val {color: #7a5306;}
.dec.bad  {background: #F6DCD5; border-color: #C8322A !important; box-shadow: 4px 4px 0 #C8322A;}
.dec.bad .val {color: #A82820;}
.chip {display:inline-block; padding: 1px 9px; border-radius: 999px; font-size: .78rem; font-weight: 600; margin-right: 4px;
       border: 1.4px solid #2b2824; background: #F7F2E6;}
.chip.CRITICO, .chip.RECHAZO {color:#A82820; border-color: #C8322A; background: #F6DCD5;}
.chip.MEDIO {color:#7a5306; border-color: #946508; background: #F3E6C4;}
.chip.FAVORABLE {color:#2F7D4F; border-color: #2F7D4F; background: #DBE9DD;}
""" + _css_tonos() + """

/* ---------- métricas como fichas ---------- */
[data-testid="stMetric"] {background: #F7F2E6; border: 1.4px solid #1B1A17; border-radius: 10px; padding: .7rem .9rem;
  box-shadow: 3px 3px 0 #1B1A17;}
[data-testid="stMetricValue"] {font-family: "Fraunces", Georgia, serif; color: #1B1A17;}
[data-testid="stMetricLabel"] p {font: 600 .72rem "IBM Plex Mono", monospace !important; text-transform: uppercase; letter-spacing: .08em;}

/* ---------- botones: acción principal en rojo, secundaria en tinta ---------- */
[data-testid^="stBaseButton-primary"] {box-shadow: 3px 3px 0 #1B1A17; border: 1.6px solid #1B1A17 !important; font-weight: 600;}
[data-testid^="stBaseButton-secondary"], [data-testid^="stBaseLinkButton-secondary"] {background: #F7F2E6;
  border: 1.6px solid #1B1A17 !important; box-shadow: 3px 3px 0 #1B1A17; font-weight: 600;}
[data-testid^="stBaseButton-secondary"]:hover, [data-testid^="stBaseLinkButton-secondary"]:hover {background: #F6DCD5;
  color: #A82820 !important; border-color: #C8322A !important; box-shadow: 3px 3px 0 #C8322A;}
[data-testid^="stBaseButton"]:active, [data-testid^="stBaseLinkButton"]:active {transform: translate(2px, 2px); box-shadow: 1px 1px 0 #1B1A17;}
button[data-variant="segmented_control"] {background: #F7F2E6; font-weight: 600;}
button[data-variant="segmented_control"][aria-checked="true"], button[data-variant="segmented_control"][data-selected] {
  background: #C8322A !important; color: #fff !important; border-color: #1B1A17 !important;}
[data-testid="stPageLink-NavLink"] {background: #F7F2E6; border: 1.4px solid #1B1A17; border-radius: 8px; box-shadow: 2px 2px 0 #1B1A17;}
[data-testid="stPageLink-NavLink"]:hover {background: #F6DCD5; border-color: #C8322A; box-shadow: 2px 2px 0 #C8322A;}

/* ---------- pestañas ---------- */
[data-testid="stTab"] {font-weight: 500;}
[data-testid="stTab"][aria-selected="true"] {color: #C8322A; font-weight: 700;}
[data-testid="stTab"][aria-selected="true"] p {font-weight: 700;}

/* ---------- mensajes: cada tipo con su color de la guía ---------- */
[data-testid="stAlertContainer"] {border-radius: 10px; border: 1.4px solid; border-left-width: 6px;}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentInfo"]) {background: #DCE5F1; border-color: #2B5C9E; color: #1d3f6e;}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) {background: #DBE9DD; border-color: #2F7D4F; color: #1f5636;}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentWarning"]) {background: #F3E6C4; border-color: #946508; color: #5e4105;}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentError"]) {background: #F6DCD5; border-color: #C8322A; color: #8a1f18;}
[data-testid="stAlertContainer"] p {color: inherit;}

/* ---------- gráficos, tablas y diagramas sobre papel claro ---------- */
[data-testid="stPlotlyChart"], [data-testid="stGraphVizChart"] {background: #F7F2E6; border: 1.4px solid #cfc3a9; border-radius: 10px; padding: 4px;}
[data-testid="stDataFrame"] {border: 1.4px solid #1B1A17; border-radius: 8px; overflow: hidden;}

/* ---------- barra lateral en tinta ---------- */
[data-testid="stSidebarNav"] a[aria-current="page"] {background: rgba(239,106,94,.16); box-shadow: inset 4px 0 0 #EF6A5E;}
[data-testid="stSidebarNav"] a[aria-current="page"] span {color: #FFFFFF; font-weight: 700;}
[data-testid="stSidebarNav"] a:hover {background: rgba(241,234,217,.08);}
[data-testid="stNavSectionHeader"] {color: #E0B85A !important; font: 600 .72rem "IBM Plex Mono", monospace !important;
  text-transform: uppercase; letter-spacing: .12em;}
[data-testid="stSidebar"] [data-testid^="stBaseLinkButton-secondary"] {background: transparent; color: #F1EAD9; border-color: #F1EAD9 !important;
  box-shadow: 3px 3px 0 #EF6A5E;}
[data-testid="stSidebar"] [data-testid^="stBaseLinkButton-secondary"]:hover {background: #EF6A5E; color: #1B1A17 !important;}
hr {border-color: #2b2824 !important; opacity: .35;}
</style>
"""

# Llegada desde la portada: la mancha de tinta roja se retira y el contenido aparece.
CSS_LLEGADA = """
<style>
@keyframes telon {0% {opacity: 1;} 100% {opacity: 0; visibility: hidden;}}
@keyframes subir {0% {opacity: 0; transform: translateY(24px);} 100% {opacity: 1; transform: none;}}
.stApp::after {content: ""; position: fixed; inset: 0; z-index: 999999; pointer-events: none;
  background: radial-gradient(circle at 50% 55%, #c8322a 0%, #c8322a 35%, #f1ead9 75%);
  animation: telon .9s ease-out .1s forwards;}
[data-testid="stMainBlockContainer"] {animation: subir .9s cubic-bezier(.2,.7,.2,1) .25s both;}
@media (prefers-reduced-motion: reduce) {.stApp::after {display: none;} [data-testid="stMainBlockContainer"] {animation: none;}}
</style>
"""

# Portada a pantalla completa: sin barra lateral, cabecera ni márgenes.
CSS_PORTADA = """
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stHeader"],
[data-testid="stToolbar"], [data-testid="stDecoration"] {display: none !important;}
[data-testid="stMain"], [data-testid="stMainBlockContainer"], .block-container {padding: 0 !important; max-width: 100% !important;}
[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {gap: 0 !important;}
.stApp {background: #f1ead9;}
</style>
"""


def aplicar_estilos():
    st.html(CSS)


def _trazo(color: str) -> str:
    """Subrayado ondulado a mano en el color del módulo."""
    return (f'<svg class="trazo" viewBox="0 0 150 14" aria-hidden="true"><path d="M2,8 C20,2 32,13 50,7 S82,2 100,8 '
            f'S132,12 148,5" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/></svg>')


def cabecera(ceja: str, titulo: str, bajada: str = "", tono: str = "rojo"):
    """Encabezado de página: ceja en el color del módulo, título, trazo ondulado y bajada."""
    color = TONOS[tono][0]
    bajada = re.sub(r"`([^`]+)`", r"<code>\1</code>", re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", bajada))
    st.html(f'<div class="ceja" style="--t:{color}">{ceja}</div>')
    st.title(titulo, anchor=False)
    st.html(_trazo(color) + (f'<p class="bajada">{bajada}</p>' if bajada else ""))


def seccion(numero: str, titulo: str, bajada: str = "", tono: str = "rojo"):
    """Encabezado de sección con insignia numerada del color del módulo."""
    texto = f"<div><h2>{titulo}</h2>" + (f"<p>{bajada}</p>" if bajada else "") + "</div>"
    st.html(f'<div class="seccion" style="--t:{TONOS[tono][0]}"><span class="insignia">{numero}</span>{texto}</div>')


def tarjeta_decision(codigo: str, motivo: str = "", titulo: str = "Decisión"):
    texto, clase = DECISIONES.get(codigo, (codigo.replace("_", " ").capitalize(), "warn"))
    st.markdown(
        f'<div class="dec {clase}"><div class="lbl">{titulo}</div>'
        f'<div class="val">{texto}</div><div class="why">{motivo}</div></div>',
        unsafe_allow_html=True)


def texto_decision(codigo: str) -> str:
    return DECISIONES.get(codigo, (codigo, ""))[0]


def chip(nivel: str) -> str:
    return f'<span class="chip {nivel}">{nivel.capitalize()}</span>'


def lista_reglas(deducciones: list[dict], vacio: str):
    if not deducciones:
        st.caption(vacio)
        return
    filas = "".join(f"<div style='margin:3px 0'><b>{d['id']}</b> {chip(d['nivel'])} "
                    f"<code>{d['consecuencia']}</code></div>" for d in deducciones)
    st.markdown(filas, unsafe_allow_html=True)


def pesos(v: float) -> str:
    return f"$ {v:,.0f}".replace(",", ".")


def _layout(fig, alto=280, titulo=None):
    fig.update_layout(height=alto, margin=dict(l=10, r=10, t=40 if titulo else 10, b=10),
                      title=dict(text=titulo, font=dict(family="Fraunces, Georgia, serif", size=16, color=TINTA)),
                      legend=dict(orientation="h", y=-0.25), font=dict(color=TINTA),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=PAPEL_CLARO)
    fig.update_xaxes(showgrid=True, gridcolor="rgba(43,40,36,.14)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(43,40,36,.14)")
    return fig


def grafico_pertenencia(u, curvas: dict, titulo: str, marcador: float | None = None,
                        eje_x: str = "", umbrales: list[tuple[float, str]] | None = None):
    fig = go.Figure()
    for etq, curva in curvas.items():
        fig.add_trace(go.Scatter(x=u, y=curva, name=etq.capitalize(), mode="lines",
                                 line=dict(width=2.5, color=COLORES_ETIQUETA.get(etq))))
    for x, txt in umbrales or []:
        fig.add_vline(x=x, line_dash="dot", line_color="gray", annotation_text=txt,
                      annotation_position="top", annotation_font_size=10)
    if marcador is not None:
        fig.add_vline(x=marcador, line_color=COLOR_PRIMARIO, line_width=2,
                      annotation_text=f"valor = {marcador:g}", annotation_position="bottom right")
    fig.update_yaxes(range=[-0.03, 1.08], title="μ")
    fig.update_xaxes(title=eje_x)
    return _layout(fig, titulo=titulo)


def grafico_salida(res, config_salida):
    u = res["universo_salida"]
    fig = go.Figure()
    from core.difuso import curvas
    _, cs = curvas(config_salida)
    for etq, curva in cs.items():
        fig.add_trace(go.Scatter(x=u, y=curva, name=f"Riesgo {etq}", mode="lines",
                                 line=dict(width=1.5, dash="dot", color=COLORES_ETIQUETA[etq])))
    fig.add_trace(go.Scatter(x=u, y=res["agregada"], name="Salida agregada", fill="tozeroy",
                             line=dict(color=COLOR_SECUNDARIO, width=2), fillcolor="rgba(27,26,23,.18)"))
    fig.add_vline(x=res["riesgo"], line_color=COLOR_PRIMARIO, line_width=2.5,
                  annotation_text=f"centroide = {res['riesgo']:.1f}", annotation_position="top")
    fig.update_yaxes(range=[-0.03, 1.08], title="μ")
    fig.update_xaxes(title="Riesgo crediticio (0–100)")
    return _layout(fig, alto=300, titulo="Agregación (máximo) y defuzzificación (centroide)")


def grafico_lineas(x, series: dict, titulo: str, eje_x: str, eje_y: str, alto=300):
    fig = go.Figure()
    paleta = [COLOR_PRIMARIO, AZUL, ORO, VERDE, TINTA]
    for k, (nombre, y) in enumerate(series.items()):
        fig.add_trace(go.Scatter(x=x, y=y, name=nombre, mode="lines",
                                 line=dict(width=2.2, color=paleta[k % len(paleta)])))
    fig.update_xaxes(title=eje_x)
    fig.update_yaxes(title=eje_y)
    return _layout(fig, alto=alto, titulo=titulo)


def grafico_barras_h(etiquetas, valores, titulo, formato="{:.1%}", color=AZUL, alto=None):
    orden = np.argsort(valores)
    fig = go.Figure(go.Bar(x=np.asarray(valores)[orden], y=np.asarray(etiquetas)[orden], orientation="h",
                           marker_color=color, text=[formato.format(v) for v in np.asarray(valores)[orden]],
                           textposition="outside", cliponaxis=False))
    return _layout(fig, alto=alto or 40 + 30 * len(etiquetas), titulo=titulo)


def matriz_confusion(m: dict, titulo: str):
    z = [[m["vn"], m["fp"]], [m["fn"], m["vp"]]]
    txt = [[f"VN<br>{m['vn']}", f"FP<br>{m['fp']}"], [f"FN<br>{m['fn']}", f"VP<br>{m['vp']}"]]
    fig = go.Figure(go.Heatmap(z=z, x=["Sin alerta", "Alerta"], y=["Legítima", "Fraude"], text=txt,
                               texttemplate="%{text}", colorscale=[[0, PAPEL_CLARO], [1, AZUL]], showscale=False))
    fig.update_yaxes(autorange="reversed", title="Real")
    fig.update_xaxes(title="Predicción")
    return _layout(fig, alto=260, titulo=titulo)
