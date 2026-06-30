# Project Tiers — detailní kritéria

Rozhodovací rámec pro určení tier projektu. Tier ovlivňuje celý pipeline.

---

## Tier 1 · Malý nástroj

**Kritéria (všechna musí platit):**
- Jeden uživatel (jen ty)
- Žádná nebo lokální DB (SQLite, JSON soubor)
- Žádný hosting — běží lokálně nebo jako skript
- Scope je jasný a fixní — nebude růst
- Odhadovaná práce: < 1 týden

**Příklady:**
- Python skript pro automatizaci (přejmenování souborů, export dat)
- Figma plugin pro design workflow
- CLI utilita pro osobní použití
- Jednoduchý bash/node skript

**Pipeline:**
- `brainstorm` skill stačí
- `/create` volitelný (jen pro složitější skripty)
- Žádné agenty, žádný `/implement`, žádný `/git`
- Vibecoding je OK

---

## Tier 2 · Web nebo menší aplikace

**Kritéria:**
- 1–10 uživatelů (ty + možná klient / rodina / tým)
- DB potřeba (Supabase, SQLite, Postgres)
- Hosting potřeba (Vercel, Railway, NAS)
- Scope je víceméně fixní — možná drobné rozšíření
- Odhadovaná práce: 1–4 týdny

**Příklady:**
- Rezervační systém pro klienta (masér, salón)
- Landing page s admin sekcí
- Mailing systém / automatizace
- Interní nástroj pro malý tým
- Portfolio s CMS

**Pipeline:**
- `discovery` → `/create` → `/implement` (light — bez paralelních agentů)
- `/git` pro ship
- Cursor reviewer volitelný
- CLAUDE.md doporučený

---

## Tier 3 · Produkt

**Kritéria (alespoň dvě platí):**
- Víc uživatelů, potenciál růstu
- Iterativní vývoj — projekt se bude měnit měsíce/roky
- Komplexní doména (platby, notifikace, role, multi-tenant)
- Potřeba škálovat (výkon, bezpečnost, náklady)
- Odhadovaná práce: měsíce

**Příklady:**
- Payminder (interní platební/fakturační systém)
- SaaS produkt
- Platforma pro víc zákazníků
- Firemní interní systém s rolemi

**Pipeline:**
- Celý stack: `discovery` → `/create` → `/implement` (plný — T3 má 11 kroků) → `/git`
- Paralelní agenti (BE + FE + QA)
- Writer/Reviewer pattern
- Cursor jako nezávislý reviewer
- CLAUDE.md povinný
- Hooks (SessionStart, TaskCompleted, Stop)
- `/insights` pro meta-loop

---

## Časté záměny

**"Malá věc, která pak vyrostla"** → vždy začni discovery, i kdyby to vypadalo jako T1. Pokud existuje šance na růst, radši T2 pipeline od začátku než refactoring později.

**"Jen pro mě, ale online"** → pokud potřebuješ hosting (i Vercel free), jsi minimálně T2. Hosting = infrastruktura = komplexita.

**"Klientský projekt s fixním scope"** → většinou T2, i kdyby byl velký. Fixní scope bez iterací = `/implement` light bez dlouhodobého harnessu.

---

## Kdy povýšit tier

Povýšení tier = přechod na silnější pipeline. Signály:

- T1 → T2: "chci to mít online" / "přidal jsem DB" / "sdílím to s někým"
- T2 → T3: "přibyli uživatelé" / "začínám iterovat features" / "chci platby/auth/role"

Povýšení se dělá vědomě — spustí nový `discovery` s aktuálním stavem projektu.
