# CLAUDE.md Příklady

Hotové příklady pro různé stacky. Použij jako základ, uprav pro konkrétní projekt.

---

## Příklad 1 — Next.js 15 + Supabase + Vercel (T3 produkt)

```markdown
# CLAUDE.md — Payminder

> Sdílený kontext pro všechny Claude Code agenty.

## Projekt

Payminder — interní nástroj pro správu plateb a fakturace. Single-tenant, lokální provoz → postupně Vercel + Supabase.

## Tech stack

| Vrstva | Technologie |
|--------|------------|
| Frontend | Next.js 15 App Router, TypeScript, Tailwind CSS |
| Backend | Next.js API routes (Server Actions) |
| DB | SQLite + Prisma (dev) → Supabase Postgres (prod) |
| Auth | žádná (single-tenant) → Supabase Auth (prod) |
| Hosting | lokální (`npm run dev`) → Vercel + Supabase |
| Package manager | npm |

## Kritická pravidla

### Databáze — Prisma
- ✗ Nikdy neupravuj `prisma/dev.db` přímo
- ✓ Vždy `npx prisma migrate dev` po změně schématu
- ✓ Po migraci `npx prisma generate` pro aktualizaci typů

### Runtime
- ✓ Server Actions pro mutace, ne API routes pokud není nutné
- ✗ Žádné `"use client"` bez dobrého důvodu — prefer Server Components

### Obecná pravidla
- Žádný commit bez explicitního vyžádání
- Issues pouze přes `/create`

## Anti-patterns

- NETESTUJ CSS třídy, Tailwind utility, skeleton stavy
- NEPIŠ `any` typ bez komentáře proč

## Verifikační příkazy

```bash
npx tsc --noEmit
npm run build
npx vitest run
```
```

---

## Příklad 2 — Next.js 15 + Supabase + Vercel (T3 — plná produkce)

```markdown
# CLAUDE.md — [Název SaaS]

## Projekt

[Název] — [popis]. Multi-tenant SaaS, Vercel + Supabase.

## Tech stack

| Vrstva | Technologie |
|--------|------------|
| Frontend | Next.js 15 App Router, TypeScript, Tailwind CSS |
| Backend | Next.js API routes + Server Actions |
| DB | Supabase (Postgres) + Row Level Security |
| Auth | Supabase Auth |
| Hosting | Vercel (frontend) + Supabase (DB + storage) |
| Package manager | npm |

## Kritická pravidla

### Supabase RLS — KRITICKÉ
- ✗ `auth.uid()` přímo v RLS policy — per-row eval, zabíjí výkon
- ✓ `(select auth.uid())` — vyhodnotí se jednou pro celý dotaz

### Runtime u Supabase stránek
- ✓ `export const runtime = 'nodejs'` — VŽDY, nikdy Edge
- Edge runtime nemá přístup k Supabase server klientovi

### Monorepo struktura
- `apps/portal` — interní app (:3000)
- `apps/klient` — klientská app (:3001)
- `packages/shared` — sdílené UI / typy / utility
- Edituj vždy ve správné `apps/` složce

## Anti-patterns

- NETESTUJ CSS třídy, SVG strukturu, Tailwind utility
- Issues pouze přes `/create`, nikdy raw `gh issue create`
- gh body se speciálními znaky přes `--body-file`, ne inline

## Verifikační příkazy

```bash
npx tsc --noEmit
npm run build
npx vitest run --reporter=verbose
```
```

---

## Příklad 3 — Python FastAPI + SQLite (T2 nástroj)

```markdown
# CLAUDE.md — [Název nástroje]

## Projekt

[Název] — [popis]. Python backend, lokální nebo Railway hosting.

## Tech stack

| Vrstva | Technologie |
|--------|------------|
| Backend | Python 3.11+, FastAPI |
| DB | SQLite (dev) / Postgres (prod) |
| ORM | SQLAlchemy + Alembic |
| Hosting | lokální / Railway |
| Package manager | pip + venv |

## Kritická pravidla

### Databáze
- ✓ Vždy `alembic upgrade head` po změně modelů
- ✗ Nikdy neupravuj `alembic/versions/` ručně

### Python
- ✓ Vždy aktivuj venv: `source venv/bin/activate`
- ✓ Type hints povinné pro všechny funkce

## Verifikační příkazy

```bash
python -m pytest
mypy app/
```
```

---

## Příklad 4 — Rezervační systém pro klienta (T2)

```markdown
# CLAUDE.md — Rezervační systém [Klient]

## Projekt

Rezervační systém pro [masérka/salón/...]. Klienti si online rezervují termíny, admin spravuje kalendář.

## Tech stack

| Vrstva | Technologie |
|--------|------------|
| Frontend | Next.js 15 App Router, TypeScript, Tailwind |
| Backend | Next.js API routes |
| DB | Supabase (Postgres) |
| Auth | Supabase Auth (jen admin) |
| Hosting | Vercel + Supabase |
| Integrace | Google Calendar API, Resend (emaily) |
| Package manager | npm |

## Kritická pravidla

### Google Calendar
- ✓ Vždy kontroluj konflikty před vytvořením události
- ✗ Nikdy nevytvárej událost bez ověření dostupnosti

### Emaily (Resend)
- ✓ Vždy testuj s Resend sandbox před produkcí
- ✓ Email templates v `emails/` složce, ne inline HTML

## Anti-patterns

- NEPOSÍLEJ skutečné emaily v dev prostředí (použij sandbox)
- NEUPRAVUJ databázové záznamy přímo — vždy přes API

## Verifikační příkazy

```bash
npx tsc --noEmit
npm run build
```
```
