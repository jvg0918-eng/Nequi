from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from core import juego_brecha as jb
from ui.componentes import CSS_LLEGADA, TONO_MODULO, _layout, seccion

if st.session_state.pop("llegada_desde_portada", False):
    st.html(CSS_LLEGADA)

ILUSTRACION = Path(__file__).resolve().parent.parent / "assets" / "ladron_tinta.jpg"

st.html("""
<style>
.heroe h1 {font-family: "Fraunces", Georgia, serif; font-weight: 650; font-size: clamp(2.3rem, 4.6vw, 4rem); line-height: 1.02;
  margin: .2rem 0 0; letter-spacing: -.02em; color: #1b1a17;}
.heroe h1 em {font-style: normal; color: #c8322a; text-decoration: underline wavy #c8322a; text-decoration-thickness: 2px;
  text-underline-offset: 8px;}
.heroe p {color: #4a453d; font-size: clamp(1rem, 1.25vw, 1.15rem); max-width: 34em; margin-top: 1rem; line-height: 1.6;}
.heroe .nota {display: inline-block; margin-top: .6rem; transform: rotate(-2deg);}
.cifras {display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); border-top: 1.2px solid #4A453D;
  border-bottom: 1.2px solid #4A453D; margin: .6rem 0 .4rem; overflow: hidden;}
.cifras div {padding: 1rem; margin-left: -1px; border-left: 1px solid #CFC3A9;}
.cifras b {display: block; font: 600 1.9rem "Fraunces", Georgia, serif; color: #1b1a17;}
.cifras span {font: 500 .74rem "IBM Plex Mono", monospace; color: #6b6458; text-transform: uppercase; letter-spacing: .08em;}
.flujo {display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; margin: .6rem 0 .2rem;}
@media (max-width: 820px) {.flujo {grid-template-columns: minmax(0, 1fr);}}
.flujo div {position: relative; border: 1.2px solid var(--b, #CFC3A9); padding: 1rem 1.05rem; background: var(--f, #f7f2e6); box-shadow: inset 4px 0 0 var(--t, #4A453D), 0 8px 20px -14px rgba(27,26,23,.35);
  border-radius: 255px 14px 225px 14px / 14px 225px 14px 255px;}
.flujo div::after {content: "→"; position: absolute; right: -16px; top: 50%; transform: translate(50%, -50%);
  color: #c8322a; font: 700 1.6rem "Caveat", cursive;}
.flujo div:last-child::after {content: none;}
@media (max-width: 820px) {.flujo div::after {content: "↓"; right: 50%; top: auto; bottom: -16px; transform: translate(50%, 50%);}}
.flujo small {font: 600 .7rem "IBM Plex Mono", monospace; color: var(--x, #A3281F); letter-spacing: .12em; text-transform: uppercase;}
.flujo strong {display: block; font: 600 1.15rem "Fraunces", Georgia, serif; margin: .25rem 0 .35rem; color: #1b1a17;}
.flujo p {margin: 0; color: #4a453d; font-size: .9rem; line-height: 1.45;}
.flujo .fin {font: 700 1.15rem "Caveat", cursive; color: #c8322a; margin-top: .45rem;}
[class*="_mod_"] {transition: transform .2s ease;}
[class*="_mod_"]:hover {transform: translateY(-4px) rotate(-.5deg);}
.st-key-ilustracion img {mix-blend-mode: multiply; border-radius: 0;
  -webkit-mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, #000 62%, transparent 100%);
  mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, #000 62%, transparent 100%);}
</style>
""")

izq, der = st.columns([1.15, 1], gap="large", vertical_alignment="center")
with izq:
    st.html("""
<div class="heroe">
  <div class="ceja">Nequi IA · Fundamentos de IA · Universidad EIA 2026-2</div>
  <h1>Detener al ladrón <em>sin bloquear</em> a los clientes.</h1>
  <p>Cada solicitud de crédito puede venir de un cliente real o de alguien que se hace pasar por él, tirando de los
  hilos de dinero, tarjeta, clave y datos. Este proyecto combina cinco técnicas de inteligencia artificial para decidir,
  de forma auditable, a quién aprobar, a quién revisar y a quién detener. Todo sobre un caso simulado.</p>
  <span class="nota">cada hilo rojo es una señal de fraude →</span>
</div>
""")
with der, st.container(key="ilustracion"):
    st.image(str(ILUSTRACION), width="stretch")

st.html("""
<div class="cifras">
  <div><b>18</b><span>reglas de fraude y crédito</span></div>
  <div><b>0.8947</b><span>F1 del score calibrado</span></div>
  <div><b>256</b><span>combinaciones de señales</span></div>
  <div><b>0–100</b><span>riesgo difuso continuo</span></div>
</div>
""")

c1, c2, c3 = st.columns(3)
c1.page_link("vistas/juego.py", label="Jugar Brecha Nequi", icon=":material/sports_esports:")
c2.page_link("vistas/evaluar.py", label="Evaluar una solicitud", icon=":material/fact_check:")
c3.page_link("vistas/portada.py", label="Volver a la portada", icon=":material/theater_comedy:")

# ------------------------------------------------------------- 01 · problema ---
seccion("01", "El problema: todo control tiene un precio", tono="rojo")
st.markdown("Si el sistema es **estricto**, el ladrón no pasa, pero también se bloquea a clientes legítimos. Si es "
            "**laxo**, los clientes pasan… y el ladrón también. Mueve el umbral y mira qué le cuesta a Nequi.")
izq, der = st.columns([1, 1.5], gap="large")
with izq:
    umbral = st.slider("Umbral de bloqueo del sistema", 0.05, 0.70, 0.25, 0.01,
                       help="Puntaje de riesgo a partir del cual se bloquea la operación.")
    estilo = st.segmented_control("Tipo de ladrón", list(jb.ESTILOS), default="Moderado")
    estilo = estilo or "Moderado"
    r = jb.costo_exacto(umbral, jb.ESTILOS[estilo])
    m1, m2 = st.columns(2)
    m1.metric("Fraudes detenidos", f"{r['recall']:.0%}")
    m2.metric("Clientes bloqueados", f"{r['fpr']:.1%}")
    _, _, mejor = jb.curva_costo(jb.ESTILOS[estilo])
    st.caption(f"Contra este ladrón, el umbral más barato es **{mejor['umbral']:.3f}**. Los números salen de la misma "
               "lógica del juego (`core/juego_brecha.py`).")
with der:
    fig = go.Figure([
        go.Bar(y=["Costo"], x=[r["costo_fraude"] * 1000], name="Fraude que pasa", orientation="h", marker_color="#C8322A"),
        go.Bar(y=["Costo"], x=[r["costo_clientes"] * 1000], name="Clientes bloqueados", orientation="h", marker_color="#1B1A17"),
    ])
    fig.update_layout(barmode="stack")
    fig.update_xaxes(title="Costo esperado por cada 1000 transacciones", range=[0, 60])
    fig.update_yaxes(showticklabels=False)
    _layout(fig, 210).update_layout(legend=dict(orientation="h", y=1.22, x=0))
    st.plotly_chart(fig, width="stretch")
    st.caption("Ninguna barra llega a cero a la vez: por eso el proyecto busca un **equilibrio**, no un bloqueo total.")

# ---------------------------------------------------------- 02 · recorrido ---
seccion("02", "El recorrido de una solicitud", tono="azul")
st.html("""
<div class="flujo">
  <div style="--t:#C8322A;--f:#EDD8C8;--b:#DF978A;--x:#A3281F"><small>Sprint 2</small><strong>Motor de fraude</strong><p>Nueve reglas de identidad (F1–F9). Una alerta crítica o dos medias detienen el proceso.</p><p class="fin">→ rechazo o revisión</p></div>
  <div style="--t:#8C6A1E;--f:#E7DDC6;--b:#C4B085;--x:#6F5414"><small>Sprint 3</small><strong>Score calibrado</strong><p>Las mismas señales pasan por un score cuyos pesos y umbral ajustó la estrategia evolutiva (μ+λ).</p><p class="fin">→ segunda opinión</p></div>
  <div style="--t:#C8322A;--f:#EDD8C8;--b:#DF978A;--x:#A3281F"><small>Sprint 2</small><strong>Motor de crédito</strong><p>Nueve reglas financieras (C1–C9). Mora, antigüedad, ingreso mínimo y embargos son filtros rígidos.</p><p class="fin">→ decisión clásica</p></div>
  <div style="--t:#4A7657;--f:#E0DECC;--b:#A6B69E;--x:#3B6347"><small>Sprint 4</small><strong>Capa difusa</strong><p>Score, carga de la cuota y endeudamiento se combinan con lógica difusa (Mamdani).</p><p class="fin">→ riesgo 0–100</p></div>
</div>
""")
st.caption("Antes de todo esto, el Sprint 1 resuelve con A* cómo llega la tarjeta física al cliente, y el Sprint 3 pone a "
           "prueba al defensor contra un atacante que se adapta (teoría de juegos y el juego Brecha Nequi).")

# ------------------------------------------------------------ 03 · explorar ---
seccion("03", "Explora el proyecto", "Cada módulo tiene su color en toda la aplicación.", tono="oro")
MODULOS = [
    ("mod_juego", "vistas/juego.py", "Juego Brecha Nequi", ":material/sports_esports:", "Sprint 3 · última entrega",
     "Juega de ladrón o de Guardián y descubre por qué el equilibrio es mixto."),
    ("mod_evaluar", "vistas/evaluar.py", "Evaluar una solicitud", ":material/fact_check:", "Flujo integrado",
     "Pasa una solicitud por los cuatro motores y mira la decisión paso a paso."),
    ("mod_astar", "vistas/logistica.py", "Logística con A*", ":material/route:", "Sprint 1",
     "Ruta óptima de la tarjeta física en un mapa real y traza de f = g + h."),
    ("mod_se", "vistas/sistema_experto.py", "Sistema experto", ":material/rule:", "Sprint 2",
     "18 reglas con encadenamiento hacia adelante y umbrales editables."),
    ("mod_ee", "vistas/evolutivo.py", "Estrategia evolutiva", ":material/genetics:", "Sprint 3",
     "Calibra pesos y umbral del score de fraude maximizando el F1."),
    ("mod_tj", "vistas/juegos.py", "Teoría de juegos", ":material/swords:", "Sprint 3",
     "Coevolución defensor contra atacante, ε-Nash y juego de inspección."),
    ("mod_difuso", "vistas/difuso.py", "Lógica difusa", ":material/blur_on:", "Sprint 4",
     "Transiciones graduales en lugar de fronteras rígidas de crédito."),
    ("mod_val", "vistas/validacion.py", "Validación y pruebas", ":material/verified:", "Calidad",
     "Los mismos casos que verifica la suite automática de pytest."),
]
for fila in range(0, len(MODULOS), 4):
    for col, (clave, pagina, titulo, icono, sprint, texto) in zip(st.columns(4), MODULOS[fila:fila + 4]):
        tono = TONO_MODULO[pagina.split("/")[1].removesuffix(".py")]
        with col, st.container(key=f"t_{tono}_{clave}", height="stretch"):
            st.html(f'<div class="paso">{sprint}</div>')
            st.page_link(pagina, label=titulo, icon=icono)
            st.caption(texto)

# ----------------------------------------------------------- 04 · recursos ---
seccion("04", "Código y versión publicada", tono="verde")
c1, c2 = st.columns(2)
c1.link_button("Repositorio en GitHub", "https://github.com/mapsita123/TrabajoIA", icon=":material/code:", width="stretch")
c2.link_button("Aplicación publicada", "https://nequi-ia-app-un3zhq5ntx3nx4cff94ksn.streamlit.app/",
               icon=":material/open_in_new:", width="stretch")

with st.expander("Alcance y limitaciones"):
    st.markdown(
        "- Todos los datos son **simulados** y todos los parámetros son supuestos académicos de los notebooks del curso.\n"
        "- Los umbrales, pesos y reglas son exactamente los de los archivos de cada sprint. Donde faltó información, "
        "la decisión se declara en la página correspondiente y en `docs/ANALISIS.md`.\n"
        "- La numeración de los sprints (A* = 1, sistema experto = 2, evolutivos y teoría de juegos = 3, "
        "lógica difusa = 4) es una reconstrucción a partir del material entregado.")
