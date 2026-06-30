---
name: discovery
description: >
  Use when the user comes with a project or idea that will grow — not a one-off script or small utility. Czech triggers: "chci postavit appku", "mám nápad na produkt", "potřebuju systém pro X", "chci to dělat pořádně", "jde to udělat jako SaaS?", "kolik by to bylo práce?", or when the user describes something with multiple users / database / hosting / long-term development. Runs a structured discovery process — from vague idea to a solid foundation ready for /create. Always offers handoff to /create at the end. Don't use for small scripts, Figma plugins, or one-off tools — brainstorm skill is enough for those.
---

# Discovery

Structured process from idea to a prepared project foundation. The output is a `DISCOVERY.md` document + handoff to `/create` for the first issue.

**Model**: Sonnet

**Difference from `brainstorm`**: brainstorm is free-form thinking without commitment. Discovery is a decision process — at the end you know exactly what you're building, on what, how large it is, and what the first step is.

---

## Flow

Discovery has **3 phases**. Go through them in order — don't skip.

---

## Phase 1 — Brainstorm (open)

Internally call `brainstorm` skill logic: let the user describe the idea freely, help them think through the basic dimensions.

Ask about:
- **Problem** — what specifically bothers you / what do you want to solve?
- **Users** — just you, or more people? Do they pay for it?
- **Alternatives** — why not an existing solution? What are you missing in them?
- **Growth** — where do you see this in a year?

Goal of this phase: understand **why** the project exists and **what its core is**. Not features — the core.

Max 2 rounds of questions. If you have enough, proceed to Phase 2.

---

## Phase 2 — Structured decision

Based on Phase 1, go through these decisions. Where unsure, ask the user — max 2 questions at a time.

### 2a. Project tier

Determine tier — it influences the entire rest of the stack and the pipeline intensity.

| Tier | Criteria | Examples | Pipeline |
|------|----------|----------|----------|
| **T1** | Simple tool, 1 user, no DB or local file, < 1 week of work | Python script, Figma plugin, CLI utility | brainstorm is enough |
| **T2** | Web/app with DB, 1–10 users, clear scope, 1–4 weeks | Booking system, landing with admin, mailing | /create + /implement light |
| **T3** | Product with growth, more users, iterative development, months | SaaS, internal company system, platform | full pipeline · agents · Cursor review |

Always **justify** the tier with one sentence.

### 2b. Hosting & deployment

Depends on users and availability needs:

| Scenario | Recommendation |
|----------|---------------|
| Just me, locally | `npm run dev` / local SQLite — no hosting |
| Me + few people, low traffic | Vercel (frontend) + Supabase (DB + auth) — free tier sufficient |
| Production app, growth | Vercel Pro + Supabase Pro, or own VPS/NAS |
| Offline-first / privacy | Own NAS (Coolify, Dokku) + PostgreSQL |

### 2c. Tech stack

Recommend stack based on tier and hosting. Default stack:

**Frontend**: Next.js 15 App Router + TypeScript + Tailwind CSS
**Backend**: Next.js API routes (T2–T3) or standalone FastAPI/Express (if separate BE)
**DB**: Supabase/Postgres (multi-user, online) | SQLite+Prisma (local-first, single-user)
**Auth**: Supabase Auth (if Supabase) | NextAuth (if custom) | none (single-tenant local)
**Hosting**: Vercel (Next.js) | Railway/Render (Node/Python) | own NAS

If there is a strong reason to deviate from the default stack, explain why.

### 2d. MVP scope

Define **what is in the MVP** and **what is not**. This is the most important decision — it prevents bloat.

Format:
```
MVP (without which the app makes no sense):
- [ ] feature 1
- [ ] feature 2

V2 (nice to have, but not a blocker):
- [ ] feature 3

Never (explicit out of scope):
- feature 4 — why not
```

### 2e. Architectural decisions

For T3 projects: identify 2–3 key architectural decisions that will affect everything else. For example:
- Monorepo vs. separate repositories?
- Server-side rendering vs. client-side?
- Real-time updates needed?
- Multi-tenant vs. single-tenant?

For T1–T2: skip this section.

---

## Phase 3 — Discovery output

Assemble the `DISCOVERY.md` document. Always in English, ready to copy into the repository.

```markdown
# Discovery: [Project name]

## Problem & motivation
<2–3 sentences: what it solves, for whom, why now>

## Tier
**T[1/2/3]** — <one-sentence justification>

## Tech stack
| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | ... | ... |
| Backend | ... | ... |
| DB | ... | ... |
| Auth | ... | ... |
| Hosting | ... | ... |

## MVP scope
### In MVP
- [ ] ...

### V2
- [ ] ...

### Out of scope (forever)
- ...

## Architectural decisions
<T3 only, otherwise omit>
- **[Decision]**: [Choice] — [reason]

## Risks & open questions
- <what could go wrong or what we don't know yet>

## First step
<one concrete thing — what to do first, ideally framed as input for /create>
```

---

## Handoff to `/create`

After generating `DISCOVERY.md`, **always** ask:

> "Do you want to jump straight into `/create` now and build the first issue for the MVP?"

If yes: pass as context to `/create`:
- Tier from discovery
- Tech stack
- First MVP feature as input for intake questions

If no: save `DISCOVERY.md` and let the user decide when.

---

## Rules

- **Discovery is not a spec** — it doesn't create ACs or acceptance tests. That's `/create`'s job.
- **Decisions are binding** — discovery output doesn't change without a conscious reason. If the project changes, do a new discovery, don't patch the old one.
- **Tier can go up, never down** — if the project grows beyond T2, move to T3 pipeline. It doesn't work the other way.
- **Bloat stops here** — the "Out of scope (forever)" section is mandatory. Without it, discovery isn't done.

---

## References

See `references/project-tiers.md` for detailed tier criteria and real-world examples.
