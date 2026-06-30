---
name: polish
model: haiku
description: >
  Lightweight post-completion tuning loop for small UI/UX or behavior fixes after a task is already shipped or "done" — much cheaper than re-running the full /implement pipeline. Use it when the feedback is a small tweak, not new scope. Triggers: "/polish", and short follow-up feedback in Czech or English such as "doladit", "uprav to", "drobnost", "tohle ještě oprav", "tag je špatně umístěný", "po refreshi to mizí", "barva sedí ale pozice ne", "není to tam kde má být", "ještě tohle". It structures the feedback (location · current vs expected · reference), triages inline-fix vs new tiered issue, applies surgical fixes, and verifies with tsc. Prefer this over /implement for post-completion polish so the big model + full pipeline isn't burned on one-line tweaks.
---

# /polish — post-completion tuning loop

A cheap, surgical loop for the iterations that happen *after* a feature is functionally done — visual tweaks, placement, copy, small behavior fixes, matching a Figma node. The point is to NOT re-enter the heavy `/implement` pipeline (full explore → plan → phased build) or burn the large model on one-line changes.

**Model**: Haiku/Sonnet — this is small surgical work.

---

## When to use vs. not

- **Use** when the change is local and clear: a tweak to an existing component, a style/copy fix, a small behavior correction, matching a design reference.
- **Don't use** (it's scope, not polish): a new data model/migration, a new screen, a new endpoint, anything cross-cutting. That belongs in `/create` or `/implement` as a tiered issue.

---

## Step 1 — Structure the feedback

For each item the user raises, pin down three things **before touching code**:

1. **Location** — which screen / route / component (e.g. `ClientDetail` running bar, `/invoices/new` totals).
2. **Current vs. expected** — what it does now vs. what it should do.
3. **Reference** — Figma node, screenshot, or a concrete example, if any.

If the feedback is vague ("it's wrong", "doesn't fit"), ask exactly **one** targeted question to nail location + expected. Don't guess and don't kick off a broad exploration — that's how loops start.

## Step 2 — Triage each item

- **Trivial / visual / local** (1–2 files, obvious fix) → fix inline now.
- **Medium / cross-cutting / new behavior** → this isn't polish, it's scope. Spin it into a **new issue via `github-issue-creator`** with the right Tier; don't grow this loop. Tell the user you're deferring it and why.
- If there are several items, list them with your inline-vs-issue split and confirm before editing.

## Step 3 — Apply

Small, surgical `Edit`s. Respect the project's `CLAUDE.md`: preserve CRLF / non-ASCII, use Tailwind tokens, no `any`/`as`. If the change touches a **read path**, update BOTH the Server Component and the API route (the "missing on refresh" trap).

## Step 4 — Verify

- `npx tsc --noEmit`.
- **Never auto-open the browser.** After tsc passes, offer the user a choice:
  - „Chceš, abych smoke-testoval v browseru? (potřebuji schválení)" — then use chrome automation only if approved.
  - „Nebo to otestuješ sám — server běží na [URL]."
- Don't auto-commit or merge. Report what changed; leave commit/PR to the user or `/git`.
- Polish closes out a task — if the next thing is unrelated, offer `/clear` for a fresh context (long sessions stay expensive even when cached).

---

## Anti-patterns

- Re-exploring the whole codebase for a one-line fix.
- "Just one more thing" scope creep → that's a new issue, not polish.
- Running the full T3 `/implement` pipeline (subagents, checkpoints) for a tweak.
- Editing only one of two duplicated read paths.
- Going in circles: if two rounds don't converge, stop and ask for a reference (Figma / screenshot), or split it into an issue.
