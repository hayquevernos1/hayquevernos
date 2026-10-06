/* ¡Hay que vernos! — conexión con Supabase (solo la llave pública; la seguridad la dan las políticas RLS de la base) */
export const SUPABASE_URL = "https://zetdhbfpesowvpehehyt.supabase.co";
export const SUPABASE_KEY = "sb_publishable_t0NZF4QghoSzO7cJTsd2Rg_M41iabyE";
export const LAUNCH = new Date("2026-11-01T00:00:00-06:00");
export const FOUNDER_SLOTS = 100;

const headers = { apikey: SUPABASE_KEY, "Content-Type": "application/json" };

/** Inserta una fila. Devuelve {ok:true} | {ok:false, dup:true} | {ok:false, error} */
export async function insertRow(table, row) {
  try {
    const r = await fetch(`${SUPABASE_URL}/rest/v1/${table}`, {
      method: "POST",
      headers: { ...headers, Prefer: "return=minimal" },
      body: JSON.stringify(row),
    });
    if (r.ok) return { ok: true };
    if (r.status === 409) return { ok: false, dup: true };
    return { ok: false, error: await r.text() };
  } catch (e) {
    return { ok: false, error: String(e) };
  }
}

/** Llama una función de la base (RPC). Devuelve el valor o null si falla. */
export async function rpc(fn, args = {}) {
  try {
    const r = await fetch(`${SUPABASE_URL}/rest/v1/rpc/${fn}`, { method: "POST", headers, body: JSON.stringify(args) });
    return r.ok ? await r.json() : null;
  } catch {
    return null;
  }
}

/** WhatsApp a 10 dígitos (quita lada +52 / 52 / 1 y espacios). */
export function cleanPhone(v) {
  let d = String(v).replace(/\D/g, "");
  if (d.length === 13 && d.startsWith("521")) d = d.slice(3);
  else if (d.length === 12 && d.startsWith("52")) d = d.slice(2);
  return d;
}

export function countdown(now = new Date()) {
  const ms = Math.max(0, LAUNCH - now);
  return { d: Math.floor(ms / 864e5), h: Math.floor(ms / 36e5) % 24, m: Math.floor(ms / 6e4) % 60, s: Math.floor(ms / 1e3) % 60, done: ms === 0 };
}
