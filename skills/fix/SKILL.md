---
name: fix
model: sonnet
description: >
  Use when the user reports a bug, error, or broken behavior — anything where the root cause is unknown and needs investigation before editing. Czech triggers: "/fix", "nefunguje", "hází to error", "padá to", "bug", "broken", "nejde", "Internal Server Error", "nefunguje označování", or when an error message is pasted. This skill diagnoses first, fixes second — unlike /polish (which assumes known location) and /implement (which builds new features). Covers client errors, server 500s, missing migrations, wrong API calls, and env misconfigurations. Always ends with a verify step and handoff to /git.
---

# /fix — diagnose and fix bugs

For when something is broken and you don't yet know why. Investigate first, edit second.

**Model**: Sonnet — diagnosis requires reasoning, not just pattern matching.

---

## When to use vs. not

- **Use** when: an error message appears, something stopped working, behavior is wrong and the cause is unclear.
- **Don't use** for visual tweaks or small behavior changes with a known location → that's `/polish`.
- **Don't use** for new features or significant scope changes → that's `/create` + `/implement`.

---

## Pipeline (5 steps)

### Step 1 — Repro & symptom

Pin down the symptom before touching anything:

1. **Error message** — exact text, status code, where it appears (browser console, network tab, server log)
2. **Trigger** — what action causes it? (which button, route, API call)
3. **Scope** — always broken, or only sometimes? Only on prod, or also local?

If the user gave an error message, use it directly. If vague ("it doesn't work"), ask **one** targeted question.

### Step 2 — Root cause

Trace the error to its origin. Common layers to check (in order):

1. **Client** — is the API call correct? right method, URL, body shape?
2. **Server route** — does the route handle the input? try-catch present?
3. **Store / DB layer** — does the store method exist and handle the case?
4. **Database** — is the column / table missing? migration not applied?
5. **Environment** — missing env var, wrong URL, expired token?

Read only — no edits yet. Confirm the root cause before proceeding.

**Multi-layer bugs → parallel diagnosis:**

If the error could plausibly live in 2+ independent layers (e.g. server + DB, or client + server), spawn parallel agents instead of investigating sequentially:

```
Agent(general-purpose) — server diagnosis:
  Read: server/src/routes/*.ts, server/src/db/store.ts
  Question: does the route catch errors? does the store handle this input correctly?
  Output: root cause or "not here"

Agent(general-purpose) — client + DB diagnosis:
  Read: client/src/api/client.ts, supabase/migrations/*.sql
  Question: is the API call correct? is the column/table present in migrations?
  Output: root cause or "not here"
```

Collect both outputs, identify the real root cause, then proceed to Step 3. This turns a sequential 3-layer investigation into a single round.

### Step 3 — Fix

Surgical edits, minimum blast radius:

- Fix the root cause, not the symptom
- If the fix touches a **read + write path** (e.g. API route + store), update both
- If a **DB migration is needed**: apply via Supabase MCP (`apply_migration`) — don't just fix the code
- If the bug is in multiple layers (e.g. missing try-catch + missing migration), fix all layers in one pass

### Step 4 — Verify

```bash
# Server (if touched)
cd server && npm run build

# Client (always)
cd client && npm run lint   # tsc --noEmit

# Manual smoke test — describe exactly what to click/do
```

If verification fails → fix immediately, don't proceed to Step 5.

### Step 5 — Ship

Hand off to `/git`. Include in the commit message:
- `fix(scope): description` 
- Root cause in the commit body (one sentence) — helps future debugging

---

## Triage: fix inline vs. create issue

Some "bugs" turn out to be missing features or architectural gaps. Triage before fixing:

| Situation | Action |
|-----------|--------|
| Clear root cause, 1–3 files | Fix inline now |
| Root cause is a missing feature | Stop → `/create` a new issue, don't bolt it on |
| Root cause unclear after 2 investigation rounds | Stop → ask for browser DevTools screenshot or server log |
| Fix requires a DB migration | Apply migration first, then fix code |

---

## Common patterns in this stack

- **500 Internal Server Error** → server route missing try-catch, or Supabase throws and it's uncaught
- **"column X not found in schema cache"** → migration exists locally but wasn't applied to Supabase — run `apply_migration`
- **HTML response instead of JSON** → wrong `VITE_API_URL` on Vercel, hitting the frontend instead of the API
- **404 on API** → missing `https://` scheme in env var, or wrong Railway URL
- **Toggle/update silently fails** → optimistic update in `useTasks` rolled back, check server response in network tab

---

## Anti-patterns

- Fixing the symptom without finding the root cause ("wrap it in try-catch and hope")
- Applying a code fix when a missing migration is the real problem
- Editing without reading the error — always read the full stack trace first
- Going more than 2 rounds of investigation without asking the user for logs/screenshots
