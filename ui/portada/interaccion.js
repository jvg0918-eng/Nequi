// Portada interactiva: el ladrón es un botón real. Al atraparlo se envía el
// disparador «entrar» a Python, que cambia de página (vistas/portada.py).
export default function (component) {
  const { parentElement, setTriggerValue } = component;
  const raiz = parentElement.querySelector(".portada");
  if (!raiz) return;

  // Streamlit puede volver a llamar a esta función en cada ejecución:
  // se cancelan los oyentes anteriores para no duplicarlos.
  if (parentElement.__portada) parentElement.__portada.abort();
  const control = new AbortController();
  parentElement.__portada = control;
  const opciones = { signal: control.signal };

  const svg = raiz.querySelector("svg.escena");
  const ladron = raiz.querySelector("#ladron");
  const cuerpo = raiz.querySelector(".ladron .cuerpo");
  const pupilas = [...raiz.querySelectorAll(".pupila")];
  const capas = [...raiz.querySelectorAll("[data-prof]")];
  const pista = raiz.querySelector(".pista");
  const aviso = raiz.querySelector(".sr");
  const reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let estado = "espera";

  // Encuadre: en pantallas verticales la escena se recorta alrededor del ladrón.
  function encuadrar() {
    const r = raiz.getBoundingClientRect();
    const vertical = r.width / Math.max(r.height, 1) < 0.9;
    raiz.classList.toggle("vertical", vertical);
    svg.setAttribute("viewBox", vertical ? "500 230 780 670" : "0 0 1600 900");
    svg.setAttribute("preserveAspectRatio", vertical ? "xMidYMax meet" : "xMidYMax slice");
  }

  function cajaLadron() {
    const r = raiz.getBoundingClientRect();
    const c = cuerpo.getBoundingClientRect();
    return { x: c.left - r.left, y: c.top - r.top, w: c.width, h: c.height, vx: c.left + c.width / 2, vy: c.top + c.height * 0.45 };
  }

  function apuntar(cx, cy) {
    // Linterna
    const r = raiz.getBoundingClientRect();
    raiz.style.setProperty("--x", `${cx - r.left}px`);
    raiz.style.setProperty("--y", `${cy - r.top}px`);
    // Profundidad: las capas lejanas se mueven menos
    const dx = (cx - r.left) / r.width - 0.5;
    const dy = (cy - r.top) / r.height - 0.5;
    for (const capa of capas) {
      const p = Number(capa.dataset.prof) || 0;
      capa.style.transform = `translate(${-dx * p * 2}px, ${-dy * p}px)`;
    }
    // Los ojos del ladrón siguen el cursor
    for (const pupila of pupilas) {
      const m = pupila.getScreenCTM();
      if (!m) continue;
      const local = new DOMPoint(cx, cy).matrixTransform(m.inverse());
      const ox = Number(pupila.dataset.cx), oy = Number(pupila.dataset.cy);
      const ang = Math.atan2(local.y - oy, local.x - ox);
      const dist = Math.min(8, Math.hypot(local.x - ox, local.y - oy) / 30);
      pupila.setAttribute("cx", (ox + Math.cos(ang) * dist).toFixed(2));
      pupila.setAttribute("cy", (oy + Math.sin(ang) * dist * 0.75).toFixed(2));
    }
  }

  function alerta(activa) {
    if (estado !== "espera") return;
    raiz.classList.toggle("alerta", activa);
    for (const p of pupilas) p.setAttribute("r", activa ? "5.5" : "8");
  }

  function capturar() {
    if (estado !== "espera") return;
    estado = "atrapado";
    raiz.classList.add("alerta", "atrapado");
    aviso.textContent = "¡Atrapado! Entrando a la aplicación…";
    const c = cajaLadron();
    raiz.style.setProperty("--ix", `${c.vx}px`);
    raiz.style.setProperty("--iy", `${c.vy}px`);
    raiz.style.setProperty("--sx", `${c.x + c.w / 2}px`);
    raiz.style.setProperty("--sy", `${c.y + c.h * 0.45}px`);
    apuntar(c.vx, c.vy);
    setTimeout(() => raiz.classList.add("saliendo"), reducido ? 0 : 900);
    setTimeout(() => setTriggerValue("entrar", true), reducido ? 60 : 1650);
  }

  window.addEventListener("pointermove", (e) => apuntar(e.clientX, e.clientY), opciones);
  window.addEventListener("resize", encuadrar, opciones);
  ladron.addEventListener("pointerenter", () => alerta(true), opciones);
  ladron.addEventListener("pointerleave", () => alerta(false), opciones);
  ladron.addEventListener("focus", () => alerta(true), opciones);
  ladron.addEventListener("blur", () => alerta(false), opciones);
  ladron.addEventListener("click", capturar, opciones);
  ladron.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); capturar(); }
  }, opciones);

  encuadrar();
  const c = cajaLadron();
  apuntar(c.vx, c.vy);
  pista.classList.add("lista");

  return () => control.abort();
}
