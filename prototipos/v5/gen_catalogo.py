"""Genera catalogo_servicios.js a partir del Excel de Diego (Catalogo_eventos_sociales_y_empresariales.xlsx).
Unifica sinónimos de unidades y asigna a cada unidad una familia de conversión para el cotizador."""
import json, re, sys, unicodedata
import pandas as pd

SRC = sys.argv[1]
OUT = sys.argv[2]

EMO = {"Alimentos": "🍽️", "Audio, video e iluminación": "🎛️", "Bebidas y barra": "🍹", "Decoración y flores": "💐",
       "Diseño, impresión y regalos": "🎁", "Espacios y hospedaje": "🏛️", "Estructuras e infraestructura": "⛺",
       "Experiencias y actividades": "🎡", "Fotografía y contenido": "📸", "Imagen personal y ceremonias": "💄",
       "Limpieza y sostenibilidad": "♻️", "Mobiliario y equipo de banquete": "🪑", "Música y espectáculos": "🎧",
       "Personal": "🤵", "Planeación y coordinación": "📋", "Seguridad, salud y accesibilidad": "🛡️",
       "Servicios profesionales y efectos": "🎆", "Tecnología y registro": "💻", "Transporte y logística": "🚐"}

# Sinónimos → unidad canónica (lo que ve el proveedor y lo que se guarda)
SYN = {"Por invitado": "Por persona", "Por pieza (unidad)": "Por pieza", "Por pieza por evento": "Por pieza",
       "Por ración": "Por porción", "Por traslado (trayecto)": "Por viaje", "Por equipo por evento": "Por equipo",
       "Por kilogramo (kg)": "Por kilo", "Por gramo (g)": "Por gramo", "Por litro (L)": "Por litro",
       "Por metro cuadrado (m²)": "Por m²", "Por metro cuadrado por día": "Por m² por día",
       "Por metro cúbico (m³)": "Por m³", "Por metro cúbico por día": "Por m³ por día", "Por kilómetro (km)": "Por km",
       "Por ciento (100 piezas)": "Por ciento (100 piezas)", "Por docena (12 piezas)": "Por docena (12 piezas)",
       "Por millar (1,000 piezas)": "Por millar (1,000 piezas)", "Por presentación (show)": "Por show",
       "Por juego (set)": "Por juego", "Por tarima de carga (pallet)": "Por pallet", "Por kilovatio-hora (kWh)": "Por kWh"}

PERSONA = {"Por persona", "Por adulto", "Por niño", "Por usuario", "Por destinatario", "Por boleto emitido", "Por inscripción", "Por certificado"}
PAQUETE = {"Por paquete"}
PORC = {"Porcentaje del presupuesto administrado", "Porcentaje de ventas"}
EXTRA = {"Por hora extra"}
FIJO = {"Por evento", "Por proyecto", "Por servicio", "Por show", "Por sesión", "Por diseño", "Por campaña", "Por trámite",
        "Por actividad", "Por composición musical", "Por grupo", "Por ruta", "Por ubicación", "Por entrega", "Por recolección",
        "Por envío", "Por spot", "Por licencia", "Por reserva gestionada", "Por álbum", "Por video", "Por estación",
        "Por equipo participante", "Por menú", "Por viaje", "Por transacción", "Por elevación"}
ESPACIO = {"Por m²", "Por metro lineal", "Por m³", "Por m² por día", "Por m³ por día"}
TIEMPO = {"Por hora": "hora", "Por día": "dia", "Por jornada": "dia", "Por turno": "turno", "Por noche": "noche",
          "Por mes": "mes", "Por minuto de servicio": "min", "Por sala por día": "dia"}
PERSONA_T = {"Por persona por hora": "hora", "Por persona por día": "dia", "Por persona por noche": "noche"}


def time_of(u):
    for k, t in (("por hora", "hora"), ("por día", "dia"), ("por noche", "noche")):
        if u.lower().endswith(k):
            return t
    return ""


def family(u):
    if u in PERSONA: return "persona", ""
    if u in PERSONA_T: return "persona", PERSONA_T[u]
    if u in PAQUETE: return "paquete", ""
    if u in PORC: return "porcentaje", ""
    if u in EXTRA: return "extra", "hora"
    if u in TIEMPO: return "tiempo", TIEMPO[u]
    if u in ESPACIO: return "espacio", time_of(u)
    if u in FIJO: return "evento", ""
    return "cantidad", time_of(u)   # pieza, kilo, botella, equipo, vehículo, mesa…


def key(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).strip()


df = pd.read_excel(SRC)
df.columns = ["tipo", "cat", "sub", "unit"]
df = df.dropna(subset=["cat", "sub", "unit"])
for c in df.columns:
    df[c] = df[c].astype(str).str.strip()

units = {}
cats = []
for cat, g in df.groupby("cat", sort=False):
    subs = []
    for sub, h in g.groupby("sub", sort=False):
        t = set(h.tipo)
        tipo = "SE" if t >= {"Social", "Empresarial"} else ("S" if "Social" in t else "E")
        us = []
        for u in h.unit:
            if u.lower() == "otro":
                continue
            cu = SYN.get(u, u)
            if cu not in us:
                us.append(cu)
            if cu not in units:
                fam, tm = family(cu)
                units[cu] = {"fam": fam, "t": tm, "src": []}
            if u != cu and u not in units[cu]["src"]:
                units[cu]["src"].append(u)
        subs.append([sub, tipo, us])
    cats.append({"n": cat, "e": EMO.get(cat, "✨"), "s": subs})

data = {"version": "catálogo Diego · 7 oct 2026", "cats": cats,
        "units": {u: [v["fam"], v["t"]] for u, v in sorted(units.items(), key=lambda x: key(x[0]))}}
js = "/* Catálogo de servicios ¡Hay que vernos! (generado desde el Excel de Diego con gen_catalogo.py — no editar a mano).\n" \
     "   cats[].s = [subcategoría, tipo (S social · E empresarial · SE ambos), unidades permitidas]\n" \
     "   units[unidad] = [familia de conversión, tiempo]. Familias: persona · evento · tiempo · cantidad · espacio · paquete · porcentaje · extra */\n" \
     "window.HQV_SVC=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
open(OUT, "w").write(js)
fams = {}
for u, (f, t) in data["units"].items():
    fams.setdefault(f, []).append(u)
print(len(cats), "categorías,", sum(len(c["s"]) for c in cats), "subcategorías,", len(units), "unidades (antes 112)")
for f, us in fams.items():
    print(f"{f:11} {len(us):3}  {', '.join(us)}")
json.dump({u: {"familia": v["fam"], "tiempo": v["t"], "sinonimos": v["src"]} for u, v in units.items()},
          open(OUT.replace(".js", "_unidades.json"), "w"), ensure_ascii=False, indent=1)
