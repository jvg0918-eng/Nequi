"""Piezas de interfaz compartidas: estilos, etiquetas de decisión y gráficos."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

COLOR_PRIMARIO = "#C8322A"   # rojo del hilo de la ilustración (assets/ladron_tinta.jpg) y del tema
COLOR_SECUNDARIO = "#1B1A17"  # tinta negra del mismo dibujo
TINTA, PAPEL, ROJO = "#1B1A17", "#F1EAD9", "#C8322A"
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

CSS = """
<style>
@import url("https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&display=swap");
.block-container {padding-top: 3.2rem; max-width: 1180px;}
h1 {letter-spacing: -.01em;}
/* Trazo a mano: bordes de tinta con esquinas irregulares, como en la ilustración */
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] details, .dec {
  border: 1.6px solid #2b2824 !important; border-radius: 255px 14px 225px 14px / 14px 225px 14px 255px !important;}
.dec {padding: 14px 18px; margin: 4px 0 12px 0; background: #f7f2e6;}
.dec .lbl {font: 600 .74rem "IBM Plex Mono", monospace; text-transform: uppercase; letter-spacing: .1em; opacity: .7;}
.dec .val {font: 650 1.5rem "Fraunces", Georgia, serif; margin-top: 2px;}
.dec .why {font-size: .92rem; margin-top: 4px; opacity: .9;}
.dec.ok   {box-shadow: inset 4px 0 0 #2F7D4F;}
.dec.warn {box-shadow: inset 4px 0 0 #B07A10;}
.dec.bad  {box-shadow: inset 4px 0 0 #C8322A; border-color: #C8322A !important;}
.chip {display:inline-block; padding: 1px 9px; border-radius: 999px; font-size: .78rem; font-weight: 600; margin-right: 4px;
       border: 1.4px solid #2b2824; background: #f7f2e6;}
.chip.CRITICO, .chip.RECHAZO {color:#C8322A; border-color: #C8322A;}
.chip.MEDIO {color:#8a5e08; border-color: #B07A10;}
.chip.FAVORABLE {color:#2F7D4F; border-color: #2F7D4F;}
.paso, .ceja {font: 600 .74rem "IBM Plex Mono", monospace; color: #C8322A; text-transform: uppercase; letter-spacing: .14em;}
.ceja {margin-bottom: .35rem;}
.bajada {color: #4a453d; font-size: 1.08rem; max-width: 46em; margin-top: -.4rem;}
.num {font: 700 1.35rem "Caveat", cursive; color: #C8322A; letter-spacing: .02em;}
.nota {font: 600 1.35rem "Caveat", cursive; color: #C8322A;}
[data-testid="stSidebarNav"] a[aria-current="page"] {background: transparent; box-shadow: inset 3px 0 0 #C8322A;}
[data-testid="stSidebarNav"] a[aria-current="page"] span {color: #C8322A; font-weight: 600;}
[data-testid="stMetricValue"] {font-family: "Fraunces", Georgia, serif;}
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


def cabecera(ceja: str, titulo: str, bajada: str = ""):
    """Encabezado de página con la jerarquía tipográfica común (ceja · título · bajada)."""
    st.html(f'<div class="ceja">{ceja}</div>')
    st.title(titulo, anchor=False)
    if bajada:
        st.html(f'<p class="bajada">{bajada}</p>')


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
                      title=titulo, legend=dict(orientation="h", y=-0.25),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
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
    paleta = [COLOR_PRIMARIO, COLOR_SECUNDARIO, "#B07A10", "#2F7D4F", "#8A7F6C"]
    for k, (nombre, y) in enumerate(series.items()):
        fig.add_trace(go.Scatter(x=x, y=y, name=nombre, mode="lines",
                                 line=dict(width=2.2, color=paleta[k % len(paleta)])))
    fig.update_xaxes(title=eje_x)
    fig.update_yaxes(title=eje_y)
    return _layout(fig, alto=alto, titulo=titulo)


def grafico_barras_h(etiquetas, valores, titulo, formato="{:.1%}", color=COLOR_SECUNDARIO, alto=None):
    orden = np.argsort(valores)
    fig = go.Figure(go.Bar(x=np.asarray(valores)[orden], y=np.asarray(etiquetas)[orden], orientation="h",
                           marker_color=color, text=[formato.format(v) for v in np.asarray(valores)[orden]],
                           textposition="outside", cliponaxis=False))
    return _layout(fig, alto=alto or 40 + 30 * len(etiquetas), titulo=titulo)


def matriz_confusion(m: dict, titulo: str):
    z = [[m["vn"], m["fp"]], [m["fn"], m["vp"]]]
    txt = [[f"VN<br>{m['vn']}", f"FP<br>{m['fp']}"], [f"FN<br>{m['fn']}", f"VP<br>{m['vp']}"]]
    fig = go.Figure(go.Heatmap(z=z, x=["Sin alerta", "Alerta"], y=["Legítima", "Fraude"], text=txt,
                               texttemplate="%{text}", colorscale="Blues", showscale=False))
    fig.update_yaxes(autorange="reversed", title="Real")
    fig.update_xaxes(title="Predicción")
    return _layout(fig, alto=260, titulo=titulo)
