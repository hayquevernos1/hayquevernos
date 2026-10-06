# Puesta en marcha

## 1. Base de datos (una sola vez por archivo)
Supabase → **SQL Editor** → New query → pega el contenido de cada archivo de `supabase/` en orden numérico → **Run**.

## 2. Publicar el sitio en Cloudflare Pages
1. Cloudflare → **Workers & Pages** → **Create** → pestaña **Pages** → **Connect to Git**.
2. Elige GitHub → repositorio `hayquevernos1/hayquevernos`.
3. Configuración de compilación:
   - Framework preset: **None**
   - Build command: *(vacío)*
   - Build output directory: **public**
4. **Save and Deploy**. Queda en `https://<nombre>.pages.dev`. Cada cambio a `main` se publica solo.

## 3. Dominio (GoDaddy)
- Fase de pruebas: en Cloudflare Pages → Custom domains → `app.hayquevernos.com`; en GoDaddy → DNS → agrega el registro **CNAME** que indique Cloudflare.
- El dominio raíz `hayquevernos.com` se mueve el día del lanzamiento, cuidando los registros MX del correo.

## Fases
1. **Ahora:** home de dos lados, lista de fundadores (contador real), aviso para anfitriones, cotizador beta.
2. **Siguiente:** cuentas de proveedor, constructor del sitio (micrositio), fotos, insignia de fundador al 100%.
3. **1 de noviembre:** cotizador con precios reales de la red, solicitudes y avisos por WhatsApp.
4. **Después:** pagos (Stripe: tarjeta recurrente, OXXO, SPEI), calificaciones y espacio del planner.
