/* ¡Hay que vernos! · Configuración central del prototipo.
   Todo lo que cambia seguido (precios, número de WhatsApp, reglas) vive aquí y NO dentro de las pantallas. */
window.HQV_EMBEDDED = new URLSearchParams(location.search).get("shell") === "1";
window.HQV_CONFIG = {
  version: "prototipo v5 · oct 2026",
  // Precios provisionales en MXN (por definir con Diego)
  precios: {
    desbloquearProveedores: 99,     // anfitrión: contactos de proveedores
    proveedoresMasPlanner: 149,      // anfitrión: proveedores + elegir planner (un solo pago)
    plannerDespues: 99,              // anfitrión: cuota de conexión si contrata planner después (POR DEFINIR)
    organizamelo: 499,               // anfitrión: servicio consultivo
    haganmeloUstedes: 499,           // proveedor: armamos tu sitio
    proMensual: 99, proFundadorMensual: 99, descuentoAnual: 0.10   // anual = 99×12 −10% = $1,069
  },
  reglas: {
    horasRespuestaPlanner: 24,
    cambiosDePlannerGratis: 3,
    proveedoresVisiblesPorServicio: 8,
    diasRecordatorio: 75
  },
  // Número de WhatsApp para ideas y soporte (PENDIENTE: Diego lo define)
  whatsappIdeas: "525500000000",
  lanzamiento: "2026-11-01T00:00:00-06:00"
};

/* Medición: cada momento clave del journey se registra aquí.
   Hoy solo queda en dataLayer; cuando conectemos Clarity / PostHog / HubSpot, se enchufa en un solo lugar. */
window.hqvTrack = function (evento, datos) {
  try {
    (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: evento, t: Date.now() }, datos || {}));
    if (window.HQV_EMBEDDED) window.parent.postMessage({ hqv: "track", evento, datos }, "*");
  } catch (_) {}
};

/* Botón flotante de ideas por WhatsApp (se inserta solo una vez por página) */
window.hqvIdeas = function () {
  if (document.querySelector(".hqv-ideas") || window.HQV_EMBEDDED) return;
  const a = document.createElement("a");
  a.className = "hqv-ideas";
  a.href = "https://wa.me/" + window.HQV_CONFIG.whatsappIdeas + "?text=" + encodeURIComponent("Hola ¡Hay que vernos!, tengo una idea para mejorar la plataforma: ");
  a.target = "_blank"; a.rel = "noopener";
  a.setAttribute("aria-label", "Envíanos tus ideas por WhatsApp");
  a.innerHTML = '<svg viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128 24a104 104 0 0 0-91.2 154l-11.6 34.8a12 12 0 0 0 15.2 15.2l34.8-11.6A104 104 0 1 0 128 24Zm0 192a87.6 87.6 0 0 1-44.1-11.9 8 8 0 0 0-6.5-.7l-29.8 9.9 9.9-29.8a8 8 0 0 0-.7-6.5A88 88 0 1 1 128 216Z"/></svg><span>¿Ideas? Escríbenos</span>';
  document.body.appendChild(a);
};
