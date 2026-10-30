import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import busqueda as bq
from ui.componentes import AZUL, GRIS, ORO, PAPEL_CLARO, ROJO, SOMBRA, TINTA, TONOS, cabecera, seccion

cabecera("Sprint 1 · Búsqueda informada", "Logística de tarjetas con A*",
         "La tarjeta física sale de Bogotá hacia un hub regional y de ahí al barrio y al cliente. A* encuentra la ruta "
         "local más corta (f = g + h) y luego se decide en qué orden entregar.", tono="azul")

with st.expander("Fuente de los datos y vacíos declarados"):
    st.markdown(
        "- Red, costos, coordenadas, heurística por capas (h = 0.45 en el hub, 0.15 en barrios, 0 en clientes) y "
        "pesos Premium 3.0 / Regular 1.0: `mapas-reales-ciudades (1).html`.\n"
        "- **El script Python original de A* no está en la carpeta.** El costo barrio→cliente se deriva como "
        "g(cliente) − g(barrio) a partir del mismo archivo. El tronco Bogotá→hub se usa como un único tramo con su total.\n"
        "- El orden de entrega se modela como el problema 1‖Σ wᵢCᵢ con pᵢ = tiempo A* desde el hub. Con ese modelo la "
        "regla de Smith es óptima, como afirma el proyecto. Los tiempos son supuestos didácticos, no tiempos medidos.")

# ---------------------------------------------------- controles en una franja ---
with st.container(key="t_azul_controles"):
    c_ciudad, c_destino, c_vista = st.columns([1.3, 1, 1.1], gap="medium", vertical_alignment="bottom")
    ciudad = c_ciudad.segmented_control("Ciudad", list(bq.CIUDADES), default="Medellín")
    if not ciudad:
        st.stop()
    c = bq.CIUDADES[ciudad]
    grafo = bq.construir_grafo(ciudad)
    clientes = list(c["clientes"])
    destino = c_destino.selectbox("Cliente destino", clientes, format_func=lambda k: f"{k} · {c['clientes'][k][1]}")
    vista = c_vista.segmented_control("Vista", ["Red panorámica", "Mapa real"], default="Red panorámica",
                                      key="vista_astar") or "Red panorámica"
    res = bq.a_estrella(ciudad, destino)
    total_pasos = len(res.expandidos)
    paso = st.slider("Reproducir la búsqueda · paso a paso", 1, total_pasos, total_pasos,
                         key=f"paso_{ciudad}_{destino}",
                         help="Mueve el control para ver en qué orden A* saca los nodos de la lista abierta.")

# ------------------------------------------------- vista panorámica a lo ancho ---
en_ruta = set(zip(res.camino, res.camino[1:])) | set(zip(res.camino[1:], res.camino))
completo = paso == total_pasos
vistos_hasta = res.expandidos[:paso]
actual = res.expandidos[paso - 1]
fila = res.traza[paso - 1]
traza_por_nodo = {t["nodo"]: t for t in res.traza[:paso]}
aristas = []
for u, vecinos in grafo.items():
    for v, costo in vecinos.items():
        if (v, u) not in {(a_, b_) for a_, b_, _ in aristas}:
            aristas.append((u, v, costo))


def tipo_nodo(n):
    if n == "HUB":
        return "Hub (inicio)", TINTA, 30
    if n in c["barrios"]:
        return "Barrio", AZUL, 26
    return f"Cliente {c['clientes'][n][1]}", ROJO if c["clientes"][n][1] == "Premium" else GRIS, 20


def figura_red():
    """Red por capas de izquierda a derecha: Hub → Barrios → Clientes (mismo grafo y mismos costos)."""
    barrios = list(c["barrios"])
    yb = {b: 1 - 2 * i / max(len(barrios) - 1, 1) for i, b in enumerate(barrios)}
    orden_clientes = [k for b in barrios for k, v in c["clientes"].items() if v[0] == b]
    yc = {k: 1.25 - 2.5 * i / max(len(orden_clientes) - 1, 1) for i, k in enumerate(orden_clientes)}
    xy = {"HUB": (0.0, 0.0), **{b: (1.0, y) for b, y in yb.items()}, **{k: (2.0, y) for k, y in yc.items()}}
    fig = go.Figure()
    for u, v, costo in aristas:
        (x1, y1), (x2, y2) = xy[u], xy[v]
        if x1 == x2:   # barrio–barrio: arco hacia la izquierda para no tapar la columna
            ts = [i / 24 for i in range(25)]
            cx, cy = x1 - 0.22 - 0.12 * abs(y1 - y2), (y1 + y2) / 2
            xs = [(1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2 for t in ts]
            ys = [(1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2 for t in ts]
            mx, my = xs[12], ys[12]
        else:
            xs, ys = [x1, x2], [y1, y2]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        usa = completo and (u, v) in en_ruta
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(width=6 if usa else 2, color=ROJO if usa else GRIS),
                                 hoverinfo="skip", showlegend=False))
        fig.add_annotation(x=mx, y=my, text=f"{costo:g} h", showarrow=False, font=dict(size=11, color=ROJO if usa else TINTA),
                           bgcolor=PAPEL_CLARO, borderpad=2)
    fig.add_trace(go.Scatter(x=[xy[n][0] for n in vistos_hasta], y=[xy[n][1] for n in vistos_hasta], mode="markers",
                             marker=dict(size=48, color=ORO, opacity=0.35), name="Expandido por A*", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[xy[actual][0]], y=[xy[actual][1]], mode="markers",
                             marker=dict(size=60, color="rgba(0,0,0,0)", line=dict(width=3, color=ORO)),
                             name=f"Paso {paso}: {actual}", hoverinfo="skip"))
    grupos = {}
    for n in xy:
        grupos.setdefault(tipo_nodo(n), []).append(n)
    for (grupo, color, tam), nodos in grupos.items():
        sangria = "" if grupo.startswith(("Hub", "Barrio")) else "\u2002\u2002"
        textos = [f"<b>{n}</b>" + (f"<br>{sangria}<span style='font-size:11px'>f = {traza_por_nodo[n]['f']:g}</span>"
                                   if n in traza_por_nodo else "") for n in nodos]
        textos = [sangria + t for t in textos]
        fig.add_trace(go.Scatter(
            x=[xy[n][0] for n in nodos], y=[xy[n][1] for n in nodos], mode="markers+text", name=grupo,
            marker=dict(size=tam, color=color, line=dict(width=2, color=TINTA)), text=textos,
            textposition={"Hub": "middle left", "Barrio": "top center"}.get(grupo.split(" ")[0], "middle right"),
            textfont=dict(size=13, color=TINTA, family="IBM Plex Sans"),
            hovertext=[f"{n} · h = {bq.heuristica(n, ciudad)}" + (f" · g = {traza_por_nodo[n]['g']:g}" if n in traza_por_nodo else "")
                       for n in nodos], hoverinfo="text"))
    fig.add_trace(go.Scatter(x=[xy[destino][0]], y=[xy[destino][1]], mode="markers", name="Destino",
                             marker=dict(size=34, color="rgba(0,0,0,0)", line=dict(width=3, color=ROJO)), hoverinfo="skip"))
    for x, txt in ((0, "HUB<br>h = 0.45"), (1, "BARRIOS<br>h = 0.15"), (2, "CLIENTES<br>h = 0")):
        fig.add_annotation(x=x, y=1.6, text=txt, showarrow=False, font=dict(size=11, color=AZUL, family="IBM Plex Mono"))
    fig.update_xaxes(visible=False, range=[-0.5, 2.75])
    fig.update_yaxes(visible=False, range=[-1.55, 1.8])
    fig.update_layout(height=470, margin=dict(l=8, r=8, t=8, b=8), plot_bgcolor=PAPEL_CLARO, paper_bgcolor=PAPEL_CLARO,
                      legend=dict(orientation="h", x=0.01, y=-0.02, yanchor="top", font=dict(color=TINTA, size=12)),
                      dragmode=False)
    return fig


def figura_mapa():
    """Mapa geográfico real con la misma red, encuadrado automáticamente."""
    pos = {"HUB": c["hub"], **c["barrios"], **{k: v[3] for k, v in c["clientes"].items()}}
    fig = go.Figure()
    for u, v, costo in aristas:
        usa = completo and (u, v) in en_ruta
        fig.add_trace(go.Scattermap(
            lat=[pos[u][0], pos[v][0]], lon=[pos[u][1], pos[v][1]], mode="lines",
            line=dict(width=6 if usa else 2.2, color=ROJO if usa else GRIS),
            hoverinfo="text", text=f"{u} → {v}: {costo:.2f} h", showlegend=False))
    fig.add_trace(go.Scattermap(
        lat=[pos[n][0] for n in vistos_hasta], lon=[pos[n][1] for n in vistos_hasta], mode="markers",
        marker=dict(size=30, color=ORO, opacity=0.38), name="Expandido por A*", hoverinfo="skip"))
    fig.add_trace(go.Scattermap(
        lat=[pos[actual][0]], lon=[pos[actual][1]], mode="markers", marker=dict(size=40, color=ORO, opacity=0.6),
        name=f"Paso {paso}: {actual}", hovertext=f"g = {fila['g']} · h = {fila['h']} · f = {fila['f']}", hoverinfo="text"))
    grupos = {}
    for n in pos:
        grupos.setdefault(tipo_nodo(n), []).append(n)
    for (grupo, color, tam), nodos in grupos.items():
        fig.add_trace(go.Scattermap(
            lat=[pos[n][0] for n in nodos], lon=[pos[n][1] for n in nodos], mode="markers+text",
            marker=dict(size=tam * 0.6, color=color), text=nodos, textposition="top right",
            textfont=dict(size=13, color=TINTA), name=grupo,
            hovertext=[f"{n} · h = {bq.heuristica(n, ciudad)}" for n in nodos], hoverinfo="text"))
    fig.add_trace(go.Scattermap(
        lat=[pos[destino][0]], lon=[pos[destino][1]], mode="markers+text", marker=dict(size=22, color=ROJO),
        text=[f"Destino · {destino}"], textposition="bottom right", textfont=dict(size=14, color=ROJO),
        name="Destino", hoverinfo="text", hovertext=f"{destino} · {c['clientes'][destino][1]}"))
    fig.update_layout(
        map=dict(style="carto-positron", fitbounds="locations"), height=470, margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", x=0.01, y=0.99, bgcolor="rgba(247,242,230,.92)", bordercolor=TINTA, borderwidth=1,
                    font=dict(color=TINTA, size=12)),
        paper_bgcolor=PAPEL_CLARO)
    return fig


with st.container(key="mapa_astar"):
    if vista == "Red panorámica":
        st.plotly_chart(figura_red(), width="stretch", config={"displayModeBar": False})
    else:
        st.plotly_chart(figura_mapa(), width="stretch", config={"scrollZoom": True})

# ------------------------------------------------ resultados en fichas a lo ancho ---
estado = "Ruta encontrada" if completo else f"Buscando… paso {paso} de {total_pasos}"
ruta_html = " <span class='flecha-ruta'>→</span> ".join(
    f"<span class='nodo-ruta{' fin' if i == len(res.camino) - 1 else ''}'>{n}</span>" for i, n in enumerate(res.camino))
st.html(f"""
<style>
.st-key-mapa_astar [data-testid="stPlotlyChart"] {{border: 1.2px solid #CFC3A9; box-shadow: inset 0 4px 0 {AZUL}, {SOMBRA}; padding: 0;
  overflow: hidden; border-radius: 12px;}}
.ruta {{display: flex; flex-wrap: wrap; align-items: center; gap: .45rem; margin: .4rem 0 .2rem;}}
.ruta .rotulo {{font: 600 .72rem "IBM Plex Mono", monospace; color: {AZUL}; text-transform: uppercase; letter-spacing: .1em;
  margin-right: .3rem;}}
.nodo-ruta {{background: {PAPEL_CLARO}; border: 1.2px solid #A6A093; border-radius: 999px; padding: .15rem .8rem;
  font-weight: 600;}}
.nodo-ruta.fin {{background: {ROJO}; color: #fff;}}
.flecha-ruta {{color: {ROJO}; font: 700 1.4rem "Caveat", cursive;}}
.estado-astar {{font: 700 1.3rem "Caveat", cursive; color: {ROJO if completo else ORO}; margin-left: auto;}}
</style>
<div class="ruta"><span class="rotulo">Ruta óptima local</span>{ruta_html}
  <span class="estado-astar">{estado}</span></div>
""")

m = st.columns(4)
fichas = [
    ("azul", "Tronco desde Bogotá", f"{c['tronco'][1]:.1f} h", c["tronco"][0]),
    ("rojo", "Costo local A*", f"{res.costo:.2f} h", f"hub → {destino}"),
    ("tinta", "Total desde Bogotá", f"{c['tronco'][1] + res.costo:.2f} h", "tronco + ruta local"),
    ("oro", "Nodos expandidos", f"{total_pasos}", f"de {len(grafo)} nodos en la red"),
]
for i, (col, (tono, etiqueta, valor, detalle)) in enumerate(zip(m, fichas)):
    with col, st.container(key=f"t_{tono}_ficha_{i}"):
        st.metric(etiqueta, valor)
        st.caption(detalle)

# ------------------------------------------------------- traza y explicación ---
seccion("01", "Traza de A* paso a paso", "Cada fila es un nodo sacado de la lista abierta, en orden de menor f.", "azul")
col_traza, col_expl = st.columns([1.5, 1], gap="large")
with col_traza:
    traza = pd.DataFrame(res.traza)
    st.dataframe(traza.style.apply(lambda r: [f"background-color: {TONOS['oro'][1]}; font-weight: 600"
                                              if r["paso"] == paso else "" for _ in r], axis=1)
                 .format({"g": "{:.2f}", "h": "{:.2f}", "f": "{:.2f}"}),
                 hide_index=True, width="stretch")
with col_expl, st.container(key="t_azul_lectura"):
    st.html(f'<div class="paso">Cómo leer el paso {paso}</div>')
    st.markdown(f"A* expande **{actual}** con **g = {fila['g']}** (horas ya recorridas desde el hub) y "
                f"**h = {fila['h']}** (estimación del resto), así que **f = {fila['f']}**.")
    st.markdown("- **g** crece con cada tramo real.\n- **h** nunca sobreestima (ver abajo), por eso la primera vez que "
                "A* expande el destino, la ruta ya es óptima.\n- Los nodos con anillo dorado en el mapa son los ya "
                "expandidos.")

# ------------------------------------------------- heurística y orden de entrega ---
seccion("02", "Heurística por capas: comprobación de admisibilidad",
        "h(n) es admisible si nunca supera el costo real mínimo h*(n) hasta un cliente.", "azul")
adm = pd.DataFrame(bq.verificar_admisibilidad(ciudad))
st.dataframe(adm, hide_index=True, width="stretch")
if adm["admisible"].all():
    st.success("La heurística es admisible en todos los nodos de esta red.")
else:
    st.error("Hay nodos donde la heurística sobreestima el costo real.")

seccion("03", "Orden de entrega: comparación de políticas",
        "Con varios clientes, ¿en qué orden entregar para minimizar Σ wᵢCᵢ? Premium pesa 3, Regular 1.", "azul")
js = bq.trabajos(ciudad)
st.dataframe(pd.DataFrame(js).rename(columns={"cliente": "Cliente", "tipo": "Tipo", "w": "Peso w",
                                              "p": "Tiempo p (h)"}).assign(**{"w / p": lambda d: d["Peso w"] / d["Tiempo p (h)"]}),
             hide_index=True, width="stretch")
pol = pd.DataFrame(bq.comparar_politicas(ciudad))
opt_astar = bq.a_estrella_secuencia(js)
opt_fb = bq.fuerza_bruta(js)
pol = pd.concat([pol, pd.DataFrame([
    {"politica": "A* sobre permutaciones", "secuencia": " → ".join(opt_astar["secuencia"]), "costo": opt_astar["costo"]},
    {"politica": f"Fuerza bruta ({opt_fb['permutaciones']} permutaciones)", "secuencia": " → ".join(opt_fb["secuencia"]),
     "costo": opt_fb["costo"]}])])
st.dataframe(pol.rename(columns={"politica": "Política", "secuencia": "Secuencia", "costo": "Σ wᵢCᵢ"}),
             hide_index=True, width="stretch")
wspt = pol.iloc[2]["costo"]
if abs(wspt - opt_fb["costo"]) < 1e-9:
    st.success(f"La política ponderada (WSPT, ordenar por w/p de mayor a menor) alcanza el óptimo global "
               f"Σ wᵢCᵢ = {wspt:.2f}, igual que A* ({opt_astar['expandidos']} estados expandidos) y que la fuerza bruta.")
