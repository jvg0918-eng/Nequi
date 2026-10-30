# Nequi IA · Sistema inteligente de originación de crédito y antifraude

Aplicación Streamlit que integra en un solo flujo el proyecto semestral de **Fundamentos de IA**
(Universidad EIA, 2026-2), aplicado a un caso **ficticio** de Nequi:

| Sprint | Técnica | Qué hace en la aplicación |
|---|---|---|
| 1 | Búsqueda informada (A\*) | Ruta de entrega de la tarjeta física (Bogotá → hub → barrio → cliente) y orden de entrega óptimo (regla de Smith, verificada con A\* y fuerza bruta). |
| 2 | Sistema experto | 18 reglas de fraude (F1–F9) y crédito (C1–C9) con encadenamiento hacia adelante y cortocircuito de seguridad. |
| 3 | Estrategia evolutiva (μ+λ) | Calibra los pesos y el umbral del score de fraude (fitness = F1-score). |
| 3 | Teoría de juegos + coevolución | Defensor contra atacante con pagos económicos; equilibrio verificado con ε-Nash, matriz de pagos y juego de inspección 2×2. |
| 3 | Juego «Brecha Nequi» (última entrega) | El juego original embebido en la app, con una introducción visual y explicaciones calculadas con su misma lógica (mejor respuesta, curva de costo por umbral, ciclo sin Nash puro, equilibrio mixto). |
| 4 | Lógica difusa (Mamdani) | Reemplaza las fronteras rígidas de score, carga de la cuota y DTI por un riesgo continuo de 0 a 100, con una zona de revisión manual. |

## Experiencia

1. **Portada interactiva.** La app abre con una escena nocturna: un ladrón se acerca a la bóveda de Nequi y una cerca
   de sensores (F2–F9) lo vigila. Sus ojos siguen el cursor y la linterna ilumina donde apuntas. Al hacer clic en él
   (o pulsar Enter con el foco), queda «¡Atrapado!» y un telón magenta lleva a la página principal.
2. **Inicio.** Presenta el problema (bloquear fraude cuesta clientes; se puede probar con un umbral en vivo calculado
   con la lógica del juego), el recorrido de una solicitud, acceso a cada módulo y enlaces al repositorio y a la app.
3. **Juego Brecha Nequi.** A · introducción visual y reglas, B · el juego original jugable dentro de la página,
   C · explicaciones calculadas con su misma lógica (con exploradores interactivos del umbral y del equilibrio mixto),
   D · qué lógica comparte con el resto del proyecto y qué relación es solo conceptual, E · preguntas de comprobación.

**Diseño.** La portada toma de *Don't Board Me* la idea de una entrada lúdica, con un personaje ilustrado que es la
acción principal. El resto de la app toma de *Prometheus Fuels* la sobriedad técnica: fondo oscuro, cejas en
monoespaciada, títulos grandes con serifa, secciones numeradas y pocas animaciones. La paleta (magenta y violeta
Nequi, oro y verde) y las tipografías (Fraunces, IBM Plex Sans y Mono) son las del juego, así que la portada, la app
y el juego se ven como una sola pieza. El tema está en `.streamlit/config.toml`.

> Todos los datos son simulados y todos los parámetros son supuestos académicos. No se usan datos ni sistemas reales de Nequi.

## Flujo de una solicitud

1. **Motor de fraude (S2).** Una alerta crítica o dos medias → rechazo; una media → revisión manual. En esos casos el flujo termina.
2. **Score calibrado (S3).** Segunda opinión sobre las mismas señales; si contradice al motor de reglas, se marca para el analista.
3. **Motor de crédito (S2).** Su decisión clásica se muestra siempre. Mora, antigüedad laboral, ingreso mínimo y embargo siguen siendo filtros rígidos.
4. **Capa difusa (S4).** Riesgo de 0 a 100: bajo → aprobado, medio → revisión manual, alto → rechazo.

El análisis completo (síntesis de cada sprint, mapa de integración, contradicciones encontradas y justificación de la
lógica difusa) está en [`docs/ANALISIS.md`](docs/ANALISIS.md).

## Requisitos

- Python 3.10 o superior (probado con 3.11 y 3.13)
- Streamlit 1.66 o superior (la portada usa `st.components.v2`)
- Dependencias en `requirements.txt` (Streamlit, NumPy, pandas, Plotly)

## Ejecución local

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate     ·     macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La aplicación abre en `http://localhost:8501`.

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest -q
```

Las pruebas usan los mismos casos de la página **Validación y pruebas** (`core/casos_prueba.py`) y además verifican
que el código reproduce los resultados de los notebooks: EE con F1 = 0.8947 y umbral 0.2924, y coevolución v2 con
umbral 0.193.

## Estructura del repositorio

```
TrabajoIA/
├── app.py                    # Punto de entrada: configuración, navegación y enlaces
├── core/                     # Lógica de negocio (sin dependencia de Streamlit)
│   ├── busqueda.py           # S1 · grafo, A*, heurística por capas, políticas de entrega
│   ├── sistema_experto.py    # S2 · motor de inferencia, reglas F/C, presets
│   ├── evolutivo.py          # S3 · estrategia evolutiva (μ+λ) del score de fraude
│   ├── teoria_juegos.py      # S3 · coevolución con pagos económicos (v2) y análisis de equilibrio
│   ├── teoria_juegos_v4.py   # S3 · versión simplificada v4 (supuestos propios)
│   ├── difuso.py             # S4 · funciones de pertenencia, reglas y Mamdani
│   ├── juego_brecha.py       # Lógica exacta del juego Brecha Nequi para las explicaciones
│   ├── integracion.py        # Flujo integrado S2 → S3 → S2 → S4 y validación de entradas
│   └── casos_prueba.py       # Casos de prueba compartidos por la UI y pytest
├── ui/
│   ├── componentes.py        # Estilos, tarjetas de decisión y gráficos
│   ├── estado.py             # Estado de sesión y caché de cálculos
│   └── portada/              # Portada: escena.html, estilo.css, interaccion.js (componente st.components.v2)
├── assets/brecha_nequi.html  # Juego de la última entrega (copia sin cambios)
├── vistas/                   # Una página por sección (portada.py es la página por defecto)
├── tests/                    # test_casos.py (lógica) y test_interfaz.py (portada y juego)
├── docs/ANALISIS.md
├── .streamlit/config.toml
├── requirements.txt
└── requirements-dev.txt
```

## Despliegue en Streamlit Community Cloud

1. El código está en [github.com/mapsita123/TrabajoIA](https://github.com/mapsita123/TrabajoIA). Incluye la carpeta
   `.streamlit/` (tema visual): si subes archivos desde la web de GitHub, verifica que esa carpeta oculta también se suba.
2. Entra a [share.streamlit.io](https://share.streamlit.io) con la cuenta de GitHub y elige **Create app**.
3. Selecciona el repositorio, la rama `main` y el archivo principal `app.py`.
4. Pulsa **Deploy**. Streamlit instala `requirements.txt` automáticamente.

La aplicación no usa credenciales ni secretos. `.streamlit/secrets.toml` está en `.gitignore` por si se agregan después.

## Notas de rendimiento

- La estrategia evolutiva tarda unos segundos la primera vez y queda en caché.
- La coevolución v2 con el test ε-Nash tarda entre 20 y 30 s; la v4, unos 45 s. Ambas quedan en caché por combinación de parámetros.
