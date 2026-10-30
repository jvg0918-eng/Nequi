import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import juego_brecha as jb
from ui.componentes import COLOR_PRIMARIO, COLOR_SECUNDARIO, cabecera, _layout

cabecera("Sprint 3 · Juego de la última entrega", "Brecha Nequi",
         "Un ninja intenta robar y el Guardián de Nequi lo detiene. Cada misión convierte en jugada un concepto del "
         "proyecto: el costo de cada señal, el umbral de decisión, la estrategia evolutiva y el equilibrio de Nash.")
st.html('<div class="num">A · ANTES DE JUGAR</div>')

# ============================================================ A. INTRODUCCIÓN ===
ESCENA = """
<svg viewBox="0 0 760 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Escena del juego: el ninja recoge señales y cruza el arco de revisión del Guardián" style="width:100%;height:auto;max-height:260px">
  <rect x="2" y="2" width="756" height="226" rx="10" fill="#f7f2e6" stroke="#2b2824" stroke-width="1.6"/>
  <g fill="none" stroke="#2b2824" stroke-width="1.4" stroke-linecap="round" opacity=".55">
    <path d="M40,180 L40,72 L98,70 L100,180 M120,180 L121,102 L164,100 L165,180 M520,180 L521,62 L588,60 L590,180 M610,180 L611,96 L658,95 L660,180"/>
    <path d="M52,90 h10 M76,90 h10 M52,112 h10 M76,112 h10 M534,82 h10 M560,82 h10 M534,104 h10"/>
  </g>
  <path d="M12,181 Q200,177 380,182 T748,180" fill="none" stroke="#2b2824" stroke-width="2" stroke-linecap="round"/>
  <text x="70" y="178" font-size="54">🥷</text>
  <path d="M120,150 C160,90 200,170 240,110 S320,160 360,105 S420,120 440,90" fill="none" stroke="#c8322a" stroke-width="2.4" stroke-linecap="round"/>
  <g font-size="26"><text x="175" y="150">📱</text><text x="235" y="110">⚡</text><text x="295" y="150">🌐</text><text x="355" y="110">🔑</text></g>
  <g font-family="Caveat, cursive" font-size="17" fill="#c8322a" text-anchor="middle" font-weight="700"><text x="190" y="172">+0.6</text><text x="250" y="132">+0.6</text><text x="310" y="172">+0.6</text><text x="370" y="132">+0.6</text></g>
  <text x="430" y="66" font-size="26">👁</text><path d="M441,74 L441,178" stroke="#c8322a" stroke-width="2" stroke-dasharray="5 5"/>
  <text x="441" y="44" font-family="Caveat, cursive" font-size="17" fill="#4a453d" text-anchor="middle">F10 · no la controlas</text>
  <path d="M505,180 L506,32 Q531,18 556,32 L557,180" fill="none" stroke="#1b1a17" stroke-width="3" stroke-linecap="round"/>
  <text x="531" y="16" font-family="Caveat, cursive" font-size="17" fill="#1b1a17" text-anchor="middle">revisión: puntaje vs umbral</text>
  <text x="640" y="178" font-size="60" transform="translate(1280,0) scale(-1,1)">🛡️</text>
  <text x="670" y="112" font-family="Caveat, cursive" font-size="17" fill="#4a453d" text-anchor="middle">Guardián Nequi</text>
</svg>
"""

intro_izq, intro_der = st.columns([1.15, 1], gap="large")
with intro_izq:
    st.markdown(ESCENA, unsafe_allow_html=True)
with intro_der:
    st.markdown("##### Objetivo")
    st.markdown("Ver, jugando, por qué un sistema antifraude no puede bloquearlo todo, por qué el atacante tampoco puede "
                "activar todas las señales, y por qué el equilibrio entre ambos es **mixto**.")
    st.markdown("##### Reglas fundamentales")
    st.markdown(
        "- Cada señal F2–F9 que recoge el ninja **suma +0.6 al botín**, pero también **sube su puntaje de riesgo**.\n"
        "- El Guardián **bloquea si el puntaje supera su umbral**. La biometría falsa (🎭) bloquea siempre.\n"
        "- **F10** (👁) aparece en el 40 % de los fraudes y el ninja no la controla.\n"
        "- Nequi paga por el fraude que deja pasar (× 2 %) **y** por cada cliente legítimo que bloquea (× 98 % × 0.15).")

st.markdown("##### Las cuatro misiones")
cols = st.columns(4)
for col, (icono, titulo, juegas, concepto) in zip(cols, [
    ("🥷", "1 · El precio de cada poder", "Juegas de ninja", "Trade-off botín/riesgo y pagos de cada bando"),
    ("🛡️", "2 · El umbral de Nequi", "Juegas de Guardián", "Costo por falsos positivos, suma no cero y mejor respuesta"),
    ("🧬", "3 · El Guardián aprende", "Juegas de ninja", "Estrategia evolutiva (μ+λ), coevolución y convergencia"),
    ("🎲", "4 · Duelo simultáneo", "Eliges personaje", "Ciclo sin Nash puro, equilibrio mixto e indiferencia"),
]):
    with col, st.container(border=True):
        st.markdown(f"### {icono}")
        st.markdown(f"**{titulo}**")
        st.caption(f"{juegas} · {concepto}")

with st.expander("Cómo empezar a jugar", expanded=False):
    st.markdown(
        "1. Haz **clic sobre el escenario** del juego para que reciba el teclado.\n"
        "2. **Teclado:** ← → avanzar · ↑ saltar · Espacio atacar · Enter siguiente · R reiniciar · 1–4 cambiar de misión · "
        "N abrir el cuaderno. En la misión 2, ↑ ↓ mueven el umbral. En la 4, A/S o E/L eligen la jugada y D lanza un dado con tu mezcla.\n"
        "3. **Celular o tableta:** usa los botones táctiles que aparecen debajo del escenario.\n"
        "4. Cada concepto que vives se desbloquea en el **cuaderno** (12 en total).")

# ================================================================ B. JUEGO ===
st.divider()
st.html('<div class="num">B · JUEGO</div>')
st.subheader("Jugar", anchor=False)
st.session_state.setdefault("partida_brecha", 0)
c1, c2, c3 = st.columns([1.4, 1, 2])
mision = c1.selectbox("Empezar en", list(jb.MISIONES), format_func=jb.MISIONES.get, key="mision_brecha")
c2.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
if c2.button("Reiniciar juego", icon=":material/restart_alt:", help="Empieza una partida nueva desde la misión elegida."):
    st.session_state["partida_brecha"] += 1
c3.caption("El juego es el de la entrega, sin cambios en sus mecánicas. Su progreso (botín, oleadas, cuaderno) vive en la "
           "partida: al reiniciar o cambiar la misión inicial empieza de cero. Dentro del juego, R reinicia solo la misión actual.")
st.iframe(jb.html_juego(mision, st.session_state["partida_brecha"]), height="content")

# ========================================================== C. EXPLICACIÓN ===
st.divider()
st.html('<div class="num">C · CÓMO FUNCIONA</div>')
st.subheader("Qué pasa por dentro y por qué", anchor=False)
st.caption("Todos los números de esta sección se calculan con la misma lógica del juego (enumeración exacta de las 256 "
           "combinaciones de señales), portada a Python en `core/juego_brecha.py`.")

t_flujo, t_m1, t_m2, t_m3, t_m4 = st.tabs(["Flujo de una jugada", "Misión 1", "Misión 2", "Misión 3", "Misión 4"])

with t_flujo:
    st.graphviz_chart("""
digraph G {
  rankdir=TB; nodesep=0.5; bgcolor="transparent"; node [shape=box, style="rounded,filled", fontname="sans-serif", fontsize=12, color="#2b2824", fontcolor="#1b1a17", penwidth=1.3];
  edge [fontname="sans-serif", fontsize=10, color="#2b2824", fontcolor="#4a453d"];
  {rank=same; a; f10;}
  a [label="Ninja elige señales\\nF2–F9 (+0.6 c/u)", fillcolor="#f6dcd5"];
  f10 [label="F10 aparece\\n(40 %, no controlable)", fillcolor="#f6dcd5"];
  bio [label="¿Biometría falsa\\n(F1)?", shape=diamond, fillcolor="#f7f2e6"];
  s [label="Puntaje = Σ pesos activos\\n÷ Σ todos los pesos", fillcolor="#f7f2e6"];
  u [label="¿Puntaje > umbral\\ndel Guardián?", shape=diamond, fillcolor="#f7f2e6"];
  b [label="Bloqueado\\nbotín 0", fillcolor="#dfe9dc"];
  p [label="Pasa\\nbotín 1 + 0.6·k", fillcolor="#f6dcd5"];
  c [label="Costo de Nequi =\\n0.02·botín + 0.98·0.15·FPR", fillcolor="#f3e6c4"];
  a -> bio; f10 -> s; bio -> b [label="sí"]; bio -> s [label="no"]; s -> u; u -> b [label="sí"]; u -> p [label="no"];
  p -> c; b -> c [label="clientes legítimos\\nbloqueados también cuestan"];
}""", width="stretch")
    st.markdown("Es el mismo esquema del flujo integrado: **F1 es un control obligatorio** y las demás señales forman un "
                "**score ponderado contra un umbral**, como el que calibra la estrategia evolutiva del Sprint 3. El pago "
                "de Nequi incluye los falsos positivos, así que **no es un juego de suma cero**.")

with t_m1:
    filas = jb.combinaciones_ninja()
    mejor = jb.mejor_combinacion(filas)
    df = pd.DataFrame(filas)
    st.markdown(f"**Pregunta del ninja:** ¿qué señales conviene recoger contra el Guardián (umbral {jb.NB['umbral']})? "
                f"Recorriendo las 256 combinaciones, la **mejor respuesta** es **{mejor['señales']}**, con un botín esperado de "
                f"**{mejor['botin_esperado']:.2f}** por intento (golpe de {mejor['valor_golpe']:.1f}). Pasa sin F10, pero si F10 "
                "aparece lo bloquean.")
    por_k = df.groupby("n_señales")["botin_esperado"].max()
    fig = go.Figure(go.Bar(x=por_k.index, y=por_k.values, marker_color=[COLOR_PRIMARIO if k == mejor["n_señales"] else COLOR_SECUNDARIO for k in por_k.index],
                           text=[f"{v:.2f}" for v in por_k.values], textposition="outside"))
    fig.update_xaxes(title="Número de señales F2–F9 encendidas", dtick=1)
    fig.update_yaxes(title="Mejor botín esperado por intento")
    st.plotly_chart(_layout(fig, 300, "Más señales no siempre es mejor"), width="stretch")
    st.caption("Con 0 señales el ninja solo se lleva el valor base. Con muchas, cada golpe vale más, pero el puntaje supera "
               "el umbral y lo bloquean siempre (barras en 0). El óptimo está en el medio: es el **trade-off** que la versión con pagos económicos introdujo frente "
               "al «ataque invisible» de las primeras versiones.")
    st.markdown("##### Prueba tu propia combinación")
    elegidas = st.multiselect("Señales que recoge el ninja", [f"{s} · {jb.PODERES[i]}" for i, s in enumerate(jb.SEÑALES) if i > 0],
                              default=[f"{s} · {jb.PODERES[i]}" for i, s in enumerate(jb.SEÑALES) if s in mejor["señales"].split(" + ")])
    idx = sorted(jb.SEÑALES.index(e.split(" · ")[0]) - 1 for e in elegidas)
    fila = df[df["señales"] == (" + ".join(jb.SEÑALES[i + 1] for i in idx) or "ninguna")].iloc[0]
    k = st.columns(4)
    k[0].metric("Valor del golpe", f"{fila['valor_golpe']:.1f}")
    k[1].metric("Puntaje sin F10", f"{fila['puntaje_sin_F10']:.3f}", f"umbral {jb.NB['umbral']}", delta_color="off")
    k[2].metric("¿Pasa?", ("sí" if fila["pasa_sin_F10"] else "no") + " sin F10 · " + ("sí" if fila["pasa_con_F10"] else "no") + " con F10")
    k[3].metric("Botín esperado", f"{fila['botin_esperado']:.2f}", f"{fila['botin_esperado'] - mejor['botin_esperado']:+.2f} vs. óptimo")

with t_m2:
    st.markdown("**Pregunta de Nequi:** ¿qué umbral cuesta menos? Depende del ninja. La curva es el costo exacto por transacción "
                "para cada umbral (fraude que pasa + clientes legítimos bloqueados).")
    fig = go.Figure()
    resumen = []
    for (nombre, pc), color in zip(jb.ESTILOS.items(), ["#2F7D4F", "#B07A10", "#C8322A"]):
        us, cs, best = jb.curva_costo(pc)
        fig.add_trace(go.Scatter(x=us, y=cs, name=f"Ninja {nombre.lower()} ({pc:.0%})", line=dict(color=color, width=2.3, shape="hv")))
        fig.add_trace(go.Scatter(x=[best["umbral"]], y=[best["costo"]], mode="markers", marker=dict(size=10, color=color, symbol="star"),
                                 showlegend=False, hovertext=f"óptimo {best['umbral']:.3f}"))
        e, l = jb.costo_exacto(jb.UMBRAL_ESTRICTO, pc), jb.costo_exacto(jb.UMBRAL_LAXO, pc)
        resumen.append({"Ninja": nombre, "Umbral óptimo": best["umbral"], "Costo óptimo": best["costo"],
                        "Costo ESTRICTO (0.15)": e["costo"], "Costo LAXO (0.40)": l["costo"],
                        "Conviene": "ESTRICTO" if e["costo"] <= l["costo"] else "LAXO"})
    fig.add_vline(x=jb.UMBRAL_ESTRICTO, line_dash="dash", line_color="gray", annotation_text="ESTRICTO")
    fig.add_vline(x=jb.UMBRAL_LAXO, line_dash="dash", line_color="gray", annotation_text="LAXO")
    fig.update_xaxes(title="Umbral del Guardián")
    fig.update_yaxes(title="Costo esperado por transacción")
    st.markdown("##### Pruébalo: mueve el umbral y elige al ninja")
    e1, e2 = st.columns([1.3, 1])
    u_sel = e1.slider("Umbral del Guardián", 0.05, 0.70, 0.25, 0.005, key="m2_umbral")
    estilo_sel = e2.radio("Ninja", list(jb.ESTILOS), index=1, horizontal=True, key="m2_estilo")
    r_sel = jb.costo_exacto(u_sel, jb.ESTILOS[estilo_sel])
    fig.add_trace(go.Scatter(x=[u_sel], y=[r_sel["costo"]], mode="markers", name="Tu elección",
                             marker=dict(size=14, color="#F1EAD9", line=dict(width=3, color=COLOR_PRIMARIO))))
    st.plotly_chart(_layout(fig, 340), width="stretch")
    _, _, opt_sel = jb.curva_costo(jb.ESTILOS[estilo_sel])
    k = st.columns(4)
    k[0].metric("Fraudes bloqueados", f"{r_sel['recall']:.0%}")
    k[1].metric("Clientes bloqueados", f"{r_sel['fpr']:.1%}")
    k[2].metric("Costo (×1000)", f"{r_sel['costo'] * 1000:.2f}",
                f"{(r_sel['costo'] - opt_sel['costo']) * 1000:+.2f} vs. óptimo", delta_color="inverse")
    k[3].metric("Umbral óptimo", f"{opt_sel['umbral']:.3f}")
    if abs(r_sel["costo"] - opt_sel["costo"]) < 1e-4:
        st.success("Diste con el umbral de menor costo contra este ninja. Ahora cambia de ninja: ¿sigue siendo el mejor?", icon="🎯")
    elif r_sel["costo_clientes"] > r_sel["costo_fraude"]:
        st.info("Aquí pesa más bloquear clientes legítimos que el fraude: sube el umbral.", icon="💡")
    else:
        st.info("Aquí pesa más el fraude que se cuela: baja el umbral.", icon="💡")
    st.dataframe(pd.DataFrame(resumen), hide_index=True, width="stretch",
                 column_config={c: st.column_config.NumberColumn(format="%.4f") for c in
                                ("Costo óptimo", "Costo ESTRICTO (0.15)", "Costo LAXO (0.40)")})
    st.caption("Las curvas tienen escalones porque los pesos son discretos: cada señal extra cruza el umbral de golpe. Contra el "
               "sigiloso conviene ser laxo (bloquear más solo genera falsos positivos); contra el agresivo, estricto. Esa dependencia "
               "es la **mejor respuesta**, y como ninguna jugada sirve contra todo, el equilibrio no está en un extremo.")

with t_m3:
    st.markdown("**El Guardián evoluciona entre oleadas** con la misma estrategia evolutiva del proyecto: μ = 6 padres, λ = 16 "
                "hijos, cruce intermedio, mutación gaussiana con σ autoadaptativo y selección (μ+λ). Su fitness es el costo "
                "contra tus últimos 4 ataques. Desde la oleada 3 aparece F10.")
    st.graphviz_chart("""
digraph G {
  rankdir=LR; bgcolor="transparent"; node [shape=box, style="rounded,filled", fontname="sans-serif", fontsize=11, color="#2b2824", fillcolor="#f7f2e6", fontcolor="#1b1a17", penwidth=1.3];
  edge [fontname="sans-serif", fontsize=10, color="#2b2824", fontcolor="#4a453d"];
  o [label="Oleada: tus 60 fraudes\\ncon las señales que elegiste", fillcolor="#f6dcd5"];
  e [label="1 · Evaluar\\n6 Guardianes vs. tus\\núltimos 4 ataques"];
  x [label="2 · Cruce intermedio\\nhijo entre dos padres"];
  m [label="3 · Mutación\\nσ' = σ·e^(τN), genes + N(0,σ')"];
  h [label="4 · 16 hijos evaluados"];
  s [label="5 · Selección (μ+λ)\\nsobreviven los 6 de menor costo"];
  g [label="Nuevo Guardián\\n(más pesos donde atacas)", fillcolor="#dfe9dc"];
  o -> e -> x -> m -> h -> s -> g; g -> o [label="siguiente oleada", style=dashed];
}""", width="stretch")
    st.markdown("- **Si repites la ruta**, el Guardián sube el peso de esas señales y tu botín cae: eso es la **convergencia**.\n"
                "- **Si cambias**, tiene que volver a aprender: la **coevolución** no tiene un ganador fijo.\n"
                "- En el juego solo evoluciona el Guardián (tú eres el atacante). En la página "
                "**3 · Teoría de juegos** evolucionan ambas poblaciones a la vez.")

with t_m4:
    eq = jb.equilibrio_inspeccion()
    filas_n, cols_n = ["ESTRICTO", "LAXO"], ["AGRESIVO", "SIGILOSO"]
    tabla = pd.DataFrame([[f"Nequi {jb.A2[i, j]:.2f} · ninja {jb.B2[i, j]:.3f}"
                           + (" ◀ MR Nequi" if eq["mejor_def"][j] == i else "") + (" ▲ MR ninja" if eq["mejor_atk"][i] == j else "")
                           for j in range(2)] for i in range(2)], index=filas_n, columns=cols_n)
    st.markdown("**Matriz de pagos del duelo** (Nequi ×1000, ninja por intento). MR = mejor respuesta.")
    st.dataframe(tabla, width="stretch")
    st.graphviz_chart("""
digraph G {
  rankdir=LR; bgcolor="transparent"; node [shape=box, style="rounded,filled", fontname="sans-serif", fontsize=11, color="#2b2824", fontcolor="#1b1a17", penwidth=1.3];
  edge [fontname="sans-serif", fontsize=10, color="#2b2824", fontcolor="#4a453d"];
  e [label="Nequi ESTRICTO", fillcolor="#e9e2d0"]; s [label="Ninja SIGILOSO", fillcolor="#f6dcd5"];
  l [label="Nequi LAXO", fillcolor="#e9e2d0"]; a [label="Ninja AGRESIVO", fillcolor="#f6dcd5"];
  e -> s [label="al ninja le conviene"]; s -> l [label="a Nequi le conviene"]; l -> a [label="al ninja le conviene"]; a -> e [label="a Nequi le conviene"];
}""", width="stretch")
    st.markdown("El ciclo nunca se cierra en una celda: **no hay equilibrio en estrategias puras**. Cada bando debe mezclar "
                "en la proporción que deja **indiferente** al otro.")
    p = np.linspace(0, 1, 101)
    ag = p * jb.B2[0, 0] + (1 - p) * jb.B2[1, 0]
    si = p * jb.B2[0, 1] + (1 - p) * jb.B2[1, 1]
    fig = go.Figure([go.Scatter(x=p, y=ag, name="Ninja AGRESIVO", line=dict(color=COLOR_PRIMARIO, width=2.3)),
                     go.Scatter(x=p, y=si, name="Ninja SIGILOSO", line=dict(color=COLOR_SECUNDARIO, width=2.3))])
    fig.add_vline(x=eq["p_estricto"], line_dash="dash", line_color="#8A7F6C",
                  annotation_text=f"p* = {eq['p_estricto']:.3f}")
    fig.update_xaxes(title="Probabilidad de que Nequi sea ESTRICTO (p)")
    fig.update_yaxes(title="Pago esperado del ninja")
    st.markdown("##### Reto: encuentra la mezcla que no deja explotar a Nequi")
    p_sel = st.slider("Probabilidad de que Nequi sea ESTRICTO", 0.0, 1.0, 0.80, 0.01, key="m4_p")
    pago_ag, pago_si = p_sel * jb.B2[0, 0] + (1 - p_sel) * jb.B2[1, 0], p_sel * jb.B2[0, 1] + (1 - p_sel) * jb.B2[1, 1]
    fig.add_vline(x=p_sel, line_color="#1B1A17", line_width=2)
    st.plotly_chart(_layout(fig, 300, "Condición de indiferencia del ninja"), width="stretch")
    if abs(pago_ag - pago_si) < 0.02:
        st.success(f"¡Equilibrio! Con p = {p_sel:.2f} al ninja le da igual atacar agresivo ({pago_ag:.3f}) o sigiloso "
                   f"({pago_si:.3f}): ya no puede aprovecharse de Nequi.", icon="⚖️")
    else:
        mejor_ninja = "AGRESIVO" if pago_ag > pago_si else "SIGILOSO"
        st.warning(f"Con p = {p_sel:.2f} el ninja siempre jugaría **{mejor_ninja}** "
                   f"({max(pago_ag, pago_si):.3f} frente a {min(pago_ag, pago_si):.3f}). Mueve p hasta que ambas líneas se crucen.",
                   icon="🥷")
    k = st.columns(4)
    k[0].metric("P(Nequi ESTRICTO) = p*", f"{eq['p_estricto']:.3f}")
    k[1].metric("P(ninja AGRESIVO) = q*", f"{eq['q_agresivo']:.3f}")
    k[2].metric("Pago del ninja en equilibrio", f"{eq['pago_ninja']:.3f}")
    k[3].metric("Pago de Nequi en equilibrio (×1000)", f"{eq['pago_nequi_x1000']:.2f}")
    st.caption("Si Nequi es estricto más del p* de las veces, al ninja le conviene ser siempre sigiloso; si lo es menos, siempre "
               "agresivo. Solo en p* le da igual, y por eso no puede explotar a Nequi. En el duelo, el rival lee tus últimas 8 "
               "jugadas: si dejas un patrón, te explota.")
    st.info("Esta matriz es la del notebook v3 que usa el juego (p* ≈ 0.533, q* ≈ 0.213). La página **3 · Teoría de juegos** "
            "calcula en vivo la versión v2 (p* ≈ 0.559, q* ≈ 0.214). Las dos coinciden en la dirección: Nequi mezcla cerca "
            "de mitad y mitad, y el ninja ataca de forma agresiva solo cerca de 1 de cada 5 veces.", icon="ℹ️")

# ============================================== D. CONEXIÓN CON EL PROYECTO ===
st.divider()
st.html('<div class="num">D · CONEXIÓN CON EL PROYECTO</div>')
st.subheader("Qué comparte el juego con el resto de la aplicación", anchor=False)
st.caption("Solo se marca como lógica compartida lo que el juego realmente usa. Lo demás es una relación conceptual.")
CONEXIONES = [
    ("Sistema experto", "vistas/sistema_experto.py", True,
     "F1 (biometría falsa) es un control obligatorio: bloquea siempre, como la regla crítica F1. Las señales F2–F9 son "
     "las mismas del motor de fraude."),
    ("Estrategia evolutiva", "vistas/evolutivo.py", True,
     "El Guardián evoluciona con (μ+λ), cruce intermedio y σ autoadaptativo. En el juego, μ = 6 y λ = 16, y su fitness es "
     "el costo contra tus últimos ataques; en el Sprint 3 la EE es (20+100) y maximiza el F1."),
    ("Teoría de juegos", "vistas/juegos.py", True,
     "Los pagos económicos (prevalencia 2 %, botín 1 + 0.6·k, costo 0.15 por cliente bloqueado) y el juego de inspección "
     "2×2 son los mismos. El juego usa la matriz del notebook v3; esa página calcula la v2."),
    ("Logística (A*)", "vistas/logistica.py", False,
     "El juego no usa A*. La mejor jugada del ninja se halla recorriendo las 256 combinaciones, el mismo papel que cumple "
     "la fuerza bruta cuando la página de logística verifica el orden óptimo que encuentra A*."),
    ("Lógica difusa", "vistas/difuso.py", False,
     "El Guardián decide con un umbral rígido: un punto más y bloquea. Esa frontera de golpe es justo la que la capa "
     "difusa del Sprint 4 reemplaza por un riesgo gradual de 0 a 100."),
]
for fila in (CONEXIONES[:3], CONEXIONES[3:]):
    for col, (nombre, pagina, comparte, texto) in zip(st.columns(3), fila):
        with col, st.container(border=True, height="stretch"):
            st.html(f'<span class="chip {"FAVORABLE" if comparte else "MEDIO"}">'
                    f'{"Lógica compartida" if comparte else "Relación conceptual"}</span>')
            st.page_link(pagina, label=nombre, icon=":material/arrow_forward:")
            st.caption(texto)

# ================================================= E. COMPRUEBA LO APRENDIDO ===
st.divider()
st.html('<div class="num">E · COMPRUEBA LO APRENDIDO</div>')
st.subheader("Cuatro preguntas rápidas", anchor=False)
st.caption("Las respuestas correctas se calculan con la lógica del juego. Si dudas, vuelve a jugar la misión indicada.")

mejor = jb.mejor_combinacion()
contra_agresivo = ("ESTRICTO (0.15)" if jb.costo_exacto(jb.UMBRAL_ESTRICTO, jb.ESTILOS["Agresivo"])["costo"]
                   <= jb.costo_exacto(jb.UMBRAL_LAXO, jb.ESTILOS["Agresivo"])["costo"] else "LAXO (0.40)")
eq = jb.equilibrio_inspeccion()
PREGUNTAS = [
    ("Misión 1", f"Contra el Guardián del juego (umbral {jb.NB['umbral']}), ¿cuántas señales F2–F9 le conviene recoger al ninja?",
     ["Ninguna", "1", "2", "3", "Las 8"], {0: "Ninguna", 8: "Las 8"}.get(mejor["n_señales"], str(mejor["n_señales"])),
     f"La mejor respuesta es {mejor['señales']}: pasa cuando F10 no aparece y deja un botín esperado de "
     f"{mejor['botin_esperado']:.2f}. Con más señales el puntaje supera el umbral."),
    ("Misión 2", "Contra un ninja agresivo, ¿qué umbral le cuesta menos a Nequi?",
     ["ESTRICTO (0.15)", "LAXO (0.40)"], contra_agresivo,
     "El agresivo activa muchas señales: el fraude que se cuela pesa más que los clientes bloqueados."),
    ("Misión 3", "Si el ninja repite siempre la misma combinación de señales, ¿qué hace el Guardián?",
     ["Nada, su umbral es fijo", "Sube el peso de esas señales y el botín cae", "Bloquea a todos los clientes"],
     "Sube el peso de esas señales y el botín cae",
     "Evoluciona contra tus últimos ataques: si no cambias, converge hacia tu ruta."),
    ("Misión 4", "En el duelo simultáneo, ¿existe un equilibrio en estrategias puras?",
     ["Sí", "No"], "Sí" if eq["puros"] else "No",
     f"Las mejores respuestas forman un ciclo. El equilibrio es mixto: Nequi es estricto con p* ≈ {eq['p_estricto']:.3f}."),
]
aciertos = 0
for i, (mision_q, pregunta, opciones, correcta, porque) in enumerate(PREGUNTAS):
    with st.container(border=True):
        st.html(f'<div class="paso">{mision_q}</div>')
        resp = st.radio(pregunta, opciones, index=None, horizontal=max(map(len, opciones)) < 20, key=f"quiz_{i}")
        if resp is not None:
            if resp == correcta:
                aciertos += 1
                st.success(f"Correcto. {porque}", icon="✅")
            else:
                st.error(f"No exactamente. {porque}", icon="↩️")
st.progress(aciertos / len(PREGUNTAS), text=f"{aciertos} de {len(PREGUNTAS)} correctas")
if aciertos == len(PREGUNTAS):
    st.balloons()
