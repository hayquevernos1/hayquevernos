-- ¡Hay que vernos! · Fase 1: listas de espera (proveedores fundadores y anfitriones)
-- Cómo usarlo: Supabase → SQL Editor → New query → pega todo este archivo → Run.
-- Seguridad: el sitio usa la llave pública (publishable). Con estas reglas, desde el sitio
-- solo se puede INSERTAR. Nadie puede leer, cambiar ni borrar datos con esa llave.
-- Tú los ves en Supabase → Table Editor.

-- 1) Proveedores que apartan su lugar de fundador
create table if not exists public.fundadores (
  id                bigint generated always as identity primary key,
  creado            timestamptz not null default now(),
  nombre            text not null check (char_length(nombre) between 2 and 80),
  negocio           text not null check (char_length(negocio) between 2 and 100),
  whatsapp          text not null unique check (whatsapp ~ '^[0-9]{10}$'),
  correo            text check (correo is null or (char_length(correo) <= 120 and correo ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$')),
  tipos             text[] not null check (cardinality(tipos) between 1 and 3 and tipos <@ array['servicios','venue','planner']),
  categoria         text check (char_length(categoria) <= 80),
  zona              text check (char_length(zona) <= 80),
  acepta_privacidad boolean not null check (acepta_privacidad),
  acepta_marketing  boolean not null default false,
  origen            text check (char_length(origen) <= 60)
);

-- 2) Anfitriones que quieren aviso el 1 de noviembre
create table if not exists public.avisos_anfitriones (
  id                bigint generated always as identity primary key,
  creado            timestamptz not null default now(),
  nombre            text not null check (char_length(nombre) between 2 and 80),
  whatsapp          text not null unique check (whatsapp ~ '^[0-9]{10}$'),
  acepta_privacidad boolean not null check (acepta_privacidad),
  acepta_marketing  boolean not null default false,
  origen            text check (char_length(origen) <= 60)
);

-- 3) Seguridad por fila: activada, y solo se permite insertar desde el sitio
alter table public.fundadores enable row level security;
alter table public.avisos_anfitriones enable row level security;

revoke all on public.fundadores, public.avisos_anfitriones from anon, authenticated;

grant insert (nombre, negocio, whatsapp, correo, tipos, categoria, zona, acepta_privacidad, acepta_marketing, origen)
  on public.fundadores to anon, authenticated;
grant insert (nombre, whatsapp, acepta_privacidad, acepta_marketing, origen)
  on public.avisos_anfitriones to anon, authenticated;

drop policy if exists "sitio puede apartar lugar" on public.fundadores;
create policy "sitio puede apartar lugar" on public.fundadores
  for insert to anon, authenticated with check (true);

drop policy if exists "sitio puede pedir aviso" on public.avisos_anfitriones;
create policy "sitio puede pedir aviso" on public.avisos_anfitriones
  for insert to anon, authenticated with check (true);

-- 4) Contador público de lugares apartados (solo devuelve el número, nunca los datos)
create or replace function public.fundadores_apartados()
returns integer
language sql
stable
security definer
set search_path = ''
as $$ select count(*)::int from public.fundadores $$;

revoke all on function public.fundadores_apartados() from public;
grant execute on function public.fundadores_apartados() to anon, authenticated;
