---
name: implement
model: sonnet
description: >
  Use when the user wants to implement an issue or feature. Czech triggers: "/implement", "implementuj issue #N", "udělej to", "napiš kód pro", "proveď implementaci", or when /create finishes a spec and the user wants to proceed. Runs explore → plan → implement → review → build per issue tier. T1 is straightforward; T3 fires the full pipeline with parallel agents, writer/reviewer, and optional Cursor review. Without this skill, agents implement without a plan or verification.
---

# /implement — from issue to finished code

Implementation orchestrator. The issue tier drives the entire workflow — T1 is simple, T3 has up to 11 steps with parallel agents.

**Golden rule**: Explore first, edit never — read first, plan next, then implement. No edits without a plan.

---

## Step 0 — Load the issue

Read the issue from input. Identify:
- **Issue number** (#N) or direct description
- **Tier** (T1 / T2 / T3) — must be in the issue from `/create`, or determine it yourself using criteria in `references/tier-routing.md`
- **Stack** from CLAUDE.md (if it exists)

### Step 0b — Branch setup (MANDATORY, always)

**Never implement directly on `main` or `master`.** Before any edits:

```bash
# 1. Check current branch
git branch --show-current

# 2. If on main/master → create and switch to a feature branch
git checkout -b issue-N-short-description
# e.g. issue-26-disable-vystavit-button
# e.g. issue-42-add-client-email

# 3. If already on a feature branch → proceed (no new branch needed)
```

Branch naming convention: `issue-N-kebab-case-title` (use the issue number and a 3–5 word slug from the title).

If the Linear issue has a `gitBranchName` field, use that instead.

If the working tree has uncommitted changes **unrelated to this issue** (from a different session or thread), stash them first: `git stash` — and note it in the summary so the user can pop them back.

Tier routing table:

| Tier | Criteria | Steps | Model |
|------|----------|-------|-------|
| **T1** 🟢 | Isolated change, 1–2 files, < 1 day | 4 | sonnet |
| **T2** 🟡 | Multiple components, coordination needed, 1–3 days | 7 | sonnet + opus |
| **T3** 🔴 | Architecture, cross-cutting, unclear solution, > 3 days | 11 | opus orchestrator |

---

## T1 Pipeline (5 steps)

For simple, isolated changes.

```
1. Explore    → read affected files (max 5)
2. Implement  → write code, verify (tsc + tests)
3. Review     → Agent(code-reviewer) with git diff — clean context, no author bias
4. Fix        → address any "fix immediately" findings from review
5. Summary    → how to test, what changed
```

**Post-implementation verification** (always):
```bash
npx tsc --noEmit     # or stack equivalent
npm run build        # if relevant
npx vitest run       # affected tests only
```

If verification fails → fix IMMEDIATELY, don't proceed.

**Step 3 — Code review (T1):**

Run the `/code-review` skill in low-effort mode — it only sees the diff, not your implementation reasoning. This eliminates author bias and catches type errors, missing edge cases, and wrong assumptions before CI does.

```
Skill(code-review, args="low"):
  Input:  current diff (git diff main...HEAD)
  Checks: type safety · missing edge cases · reuse of existing components · security
  Output: findings split into "fix immediately" vs "follow-up issue"
```

- **Fix immediately** findings → address in step 4, then re-verify tsc
- **Follow-up** findings → note in summary, create issue via /create after /git
- **No findings** → skip step 4, go straight to summary

---

## T2 Pipeline (7 steps)

For changes touching multiple components.

```
1. Explore         → read affected files (max 10)
2. Plan            → write implementation plan (save as issue comment)
3. Implement       → sequential implementation per plan
4. Verification    → tsc + build + tests
5. Code review     → Agent(code-reviewer) in clean context — medium effort
6. Final build     → clean build after addressing findings
7. Summary         → how to test, what changed, → /git
```

**Implementation plan** (step 2) contains:
- Affected files (marked new/updated/deleted)
- Step sequence (numbered)
- Risks and dependencies
- Verification procedure

**Step 5 — Code review (T2):**

Same pattern as T1 but medium effort — more files touched means higher review surface.

```
Skill(code-review, args="medium"):
  Input:  current diff (git diff main...HEAD)
  Checks: reuse · quality · efficiency · cross-component consistency · security
  Output: findings split into "fix immediately" vs "follow-up issue"
```

The skill runs in a clean context (no knowledge of what was built, only the diff). Fix all "fix immediately" findings before step 6. Follow-up findings → new issues via `/create`.

### Checkpoint system (T2 lightweight)

After each completed step, update `.claude/implement-state.md`. Progress tracking only — no agent outputs (T2 is sequential).

```markdown
# Implement State

**Issue**: #N — [title]
**Tier**: T2
**Branch**: [branch name]
**Last checkpoint**: YYYY-MM-DD HH:MM

## Pipeline steps

- [ ] 01. Explore
- [ ] 02. Plan
- [ ] 03. Implement
- [ ] 04. Verification
- [ ] 05. Code review
- [ ] 06. Final build
- [ ] 07. Summary → /git
```

Replace `[ ]` with `[x]` immediately after completing each step. Delete the file after step 07.

---

## T3 Pipeline (11 steps)

For complex changes with architectural decisions. Opus as orchestrator.

```
01. Explore              → read code, no edits
02. Analyze              → identify dependencies, risks, affected areas
03. Plan                 → implementation plan → save as issue comment
04. Phase 1 impl. (‖)   → parallel agents: foundation (migrations, types, schema)
05. Phase 1 verify       → tsc + migrations pass
06. Phase 2 impl. (‖)   → parallel agents: backend + frontend simultaneously
07. Phase 2 verify       → tsc + build + unit tests
08. Writer/Reviewer      → review in clean context (see below)
09. Tests + docs         → test-engineer + documentation-writer in parallel
10. Final build          → clean build, all tests pass
11. Summary              → how to test, what changed, → /git
```

### Checkpoint system (T3 required)

After each completed step, write state to `.claude/implement-state.md`. This file lets the `/continue` skill resume the pipeline after compaction or token limit.

**File format:**

```markdown
# Implement State

**Issue**: #N — [title]
**Tier**: T3
**Branch**: [branch name]
**Last checkpoint**: YYYY-MM-DD HH:MM

## Pipeline steps

- [ ] 01. Explore
- [ ] 02. Analyze
- [ ] 03. Plan
- [ ] 04. Phase 1 impl. (‖)
- [ ] 05. Phase 1 verify
- [ ] 06. Phase 2 impl. (‖)
- [ ] 07. Phase 2 verify
- [ ] 08. Writer/Reviewer
- [ ] 09. Tests + docs
- [ ] 10. Final build
- [ ] 11. Summary → /git

## Completed step outputs

### 03. Plan
[plan summary — affected files, step sequence, risks]

### 04. Phase 1 impl.
BE: [what changed]
FE: [what changed]

### 08. Writer/Reviewer
Findings to fix immediately: [list or "none"]
Follow-up issues: [list or "none"]

## Open review findings
[findings not yet addressed]
```

**When to update:** replace `[ ]` with `[x]` and fill the output section immediately after completing each step — not at end of phase.

**After step 11:** delete the file (`rm .claude/implement-state.md`) and continue to `/git`.

### Parallel phases (‖)

Hard dependencies wait; soft dependencies run in parallel:

```
Phase 1 (parallel):
  Task(back-end-developer)  → migrations + schema + types
  Task(front-end-developer) → skeleton + basic layout

Phase 2 (parallel):
  Task(back-end-developer)  → API routes / Server Actions
  Task(front-end-developer) → UI components + logic
  Task(data-visualization)  → charts / tables (if relevant)
```

Each agent carries its own verification:
```
npx tsc --noEmit → error? fix IMMEDIATELY
npx vitest run … → fails? fix IMMEDIATELY
```

### Writer/Reviewer pattern (step 08)

Review happens in a **clean context** — the reviewer doesn't know what the author implemented, only sees the diff. Eliminates author bias.

```
Skill(code-review, args="high"):
  - Input: current diff (git diff HEAD~1)
  - Checks: reuse of existing components · quality · efficiency · security
  - Output: list of findings (fix immediately vs. follow-up issue)
  - Findings the author won't fix → new issue via /create

Task(ui-ux-designer):  ← T3 with UI changes only
  - Input: screenshots or description of UI changes
  - Checks: design system consistency · spacing · edge cases
```

### Cursor as independent reviewer (optional)

If the user wants a Cursor review, before step 08:

1. Generate `CURSOR_REVIEW.md` in the project root:
```markdown
# Cursor Review Request

## Issue
[issue number and title]

## What changed
[brief description]

## What to check
- [ ] Logic errors the author missed
- [ ] Security risks
- [ ] Performance issues
- [ ] Edge cases in business logic

## Diff
[output of git diff HEAD~1 or link to PR]
```

2. Tell the user: *"Open Cursor, load `CURSOR_REVIEW.md`, and ask it for a review. Pass the results back to me."*
3. After receiving results, process findings the same as Writer/Reviewer output.

---

## Agents — role overview

Detailed agent prompts in the `agents/` folder.

| Agent | Use | Model |
|-------|-----|-------|
| `back-end-developer` | API, DB, migrations, Server Actions | sonnet |
| `front-end-developer` | UI components, pages, client logic | sonnet |
| `test-engineer` | Unit tests, coverage > 50% | sonnet |
| `documentation-writer` | Docs, comments, README | haiku |
| `code-review` (skill) | Diff review, quality check | opus |
| `ui-ux-designer` | UX review, design consistency | sonnet |
| `security-auditor` | Security audit (T3, optional) | opus |

---

## Evidence before assertions

Agents love to report success before it happens. Proof means:
- ✓ Green command output in terminal
- ✓ Passing tests
- ✗ The sentence "implementation is done"

Never accept completion without verification output.

---

## Output (summary)

At the end of each pipeline generate a summary:

```markdown
## Implementation summary #[N]

**What changed:**
- [file]: [what and why]

**How to test:**
1. [specific step]
2. [what to verify]

**Follow-up issues:**
- [review finding not fixed → /create]

**Next step:** /git
```

If the issue includes UI changes, **offer** (don't auto-invoke) visual verification:

> "Změna obsahuje UI — chceš spustit `/visual`? Otestuji v browseru (potřebuji schválení), nebo to otestuješ sám."

---

## Context hygiene

This is the heaviest skill — keep the context lean so long T2/T3 runs don't balloon (sessions stay expensive even when cached):
- **T2/T3:** suggest `/compact` at phase boundaries (after a phase verifies green) — the exploration/diffs from a finished phase don't need to stay in full context.
- **After the summary:** if the next task is unrelated, offer `/clear` for a fresh context rather than continuing in the same session.

---

## References

- `references/tier-routing.md` — detailed tier criteria and edge cases
- `agents/back-end-developer.md` — BE agent prompt
- `agents/front-end-developer.md` — FE agent prompt
- `agents/code-reviewer.md` — reviewer agent prompt
