---
name: claude-md-generator
description: >
  Use when the user is starting a new project and needs a CLAUDE.md — shared context for all agents. Czech triggers: "vytvoř CLAUDE.md", "nastav projekt pro Claude Code", "připrav harness", "zakládám nový projekt", or when discovery skill finishes phase 3 and the user wants to continue to setup. Runs a short intake about the project and generates a ready CLAUDE.md file to copy into the repository root. Without CLAUDE.md, agents have no shared context and repeat the same mistakes.
---

# CLAUDE.md Generator

Generates `CLAUDE.md` — shared project context for all Claude Code agents. What is learned once applies to all sessions and all agents.

**Model**: Sonnet

**Principle**: What you fix a second time, you write into CLAUDE.md. The error won't return.

---

## Workflow

### Step 1 — Intake

If coming from the `discovery` skill, you already have most answers. Just fill in the missing ones.

If starting from scratch, ask these things — max 2 rounds, max 3 questions at a time:

**Round 1 — foundation:**
- Project name and a one-sentence description (what it does, for whom)
- Tech stack (framework, DB, hosting, auth)
- Monorepo or single repo? If monorepo — what structure?

**Round 2 — domain rules (if not obvious):**
- Are there critical rules agents must never break? (RLS, runtime, naming conventions...)
- Where are the key files / directories?
- What is forbidden? (direct commits without being asked, inline test CSS classes, ...)

### Step 2 — Generate

Generate `CLAUDE.md` using the template below. Adapt the content to the project — don't fill sections that don't make sense.

---

## CLAUDE.md template

```markdown
# CLAUDE.md — [Project name]

> Shared context for all Claude Code agents. A rule here = a rule everywhere.

## Project

[Name] — [one-sentence description, for whom, what it solves]

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | [e.g. Next.js 15 App Router, TypeScript, Tailwind CSS] |
| Backend | [e.g. Next.js API routes / FastAPI] |
| DB | [e.g. Supabase (Postgres) / SQLite + Prisma] |
| Auth | [e.g. Supabase Auth / NextAuth / none] |
| Hosting | [e.g. Vercel + Supabase / local / own NAS] |
| Package manager | [npm / pnpm / yarn] |

## Project structure

[Directory structure description — only if not obvious from the stack]

```
app/              # Next.js App Router pages
components/       # shared UI components
lib/              # utilities, helpers
prisma/           # schema and migrations (if Prisma)
```

## Critical rules

> These rules must not be broken by any agent. They are the result of real mistakes.

### [Area — e.g. Database]
- ✗ [what not to do]
- ✓ [correct approach]

### [Area — e.g. Runtime]
- ✓ [specific rule]

### General rules
- No commit without explicit user request
- Create issues only via `/create`, never raw `gh issue create`
- Pass gh body with special characters via `--body-file`, not inline

## Monorepo structure (if relevant)

```
apps/[name]/      # [description]
packages/shared/  # shared types, utilities, UI
```

## Agents and models

| Agent | Model | When to use |
|-------|-------|------------|
| orchestrator | opus | /implement T3, planning |
| implementation | sonnet | regular implementation |
| /git, small tasks | haiku | commit, PR, quick tasks |

## Anti-patterns (what agents must not do)

- DON'T TEST [specific things — CSS classes, SVG structure, skeleton]
- [other project-specific anti-pattern]

## Verification commands

After every change the agent runs:
```bash
[e.g. npx tsc --noEmit]
[e.g. npm run build]
[e.g. npx vitest run]
```

## Agent documentation

[If it exists — where maps for agents are]
- `component-registry.md` — component overview
- `page-map.md` — page tree
- `db-feature-map.md` — tables ↔ features
```

---

## Generation rules

**What belongs in CLAUDE.md:**
- Rules that came from a real mistake ("what I fixed a second time")
- Domain knowledge that can't be derived from the stack (RLS patterns, specific runtime requirements)
- Project structure if it's non-standard
- Project-specific anti-patterns

**What does NOT belong in CLAUDE.md:**
- General best practices (agents already know these)
- Per-issue things (those belong in the issue/spec)
- Long tutorials or documentation (those go in `docs/`)

**Length**: CLAUDE.md should be concise — agents read it at the start of every session. Ideally under 100 lines. If it grows, move details to `.claude/docs/` and leave only a link in CLAUDE.md.

---

## After generating

Ask the user:
1. "Do you want to add any specific domain rules that you already know about?"
2. "Should I also generate the `.claude/` directory structure (hooks, docs)?"

CLAUDE.md is a living document — tell the user: *"Whenever you hit an error you had to fix manually, add a rule here."*

---

## References

See `references/claude-md-examples.md` for ready examples for various stacks.
