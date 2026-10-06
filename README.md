# ¡Hay que vernos!

La red de proveedores de fiestas de México. Dos lados de un mismo universo:

- **Proveedores** (servicios, venues y event planners independientes) crean su sitio web profesional gratis.
- **Anfitriones** pre-cotizan su fiesta por persona, gratis, y se conectan con proveedores interesados.

Sitio: https://hayquevernos.com · Lanzamiento del cotizador: **1 de noviembre de 2026**.

## Cómo está hecho (costo $0)

| Pieza | Servicio | Para qué |
|---|---|---|
| Sitio web | Cloudflare Pages (gratis) | Publica la carpeta `public/` en cada cambio a `main` |
| Base de datos | Supabase (plan Free) | Guarda registros; la seguridad está en `supabase/*.sql` |
| Código | GitHub | Este repositorio |

No hay paso de compilación: lo que está en `public/` es exactamente lo que se publica.
La única excepción es el cotizador, que se arma desde `src/cotizador/` con `python3 tools/build_cotizador.py`.

## Estructura

```
public/                 ← el sitio tal cual se publica
  index.html            ← home de dos lados (proveedor / anfitrión)
  fundadores/           ← apartar lugar de proveedor fundador
  cotizador/            ← cotizador beta (generado, no editar a mano)
  privacidad/           ← aviso de privacidad (borrador, revisar con abogado)
  js/hqv.js             ← conexión a Supabase (solo llave pública)
  css/base.css          ← colores y estilos de marca
  data/cp.bin           ← catálogo de códigos postales (SEPOMEX, gzip)
src/cotizador/          ← fuente del cotizador
supabase/               ← tablas y reglas de seguridad (correr en orden en el SQL Editor)
docs/                   ← decisiones y guía de puesta en marcha
tools/                  ← scripts sin dependencias
```

## Reglas de seguridad

- En el código solo va la llave **publishable** de Supabase (es pública por diseño).
- La llave **secret / service_role** nunca se sube al repositorio ni se pega en chats.
- Toda tabla nueva lleva RLS activado y permisos explícitos (ver `supabase/`).

## Probar en tu computadora

```
cd public && python3 -m http.server 8080
```
y abre http://localhost:8080
