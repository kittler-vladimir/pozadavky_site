---
name: visual
model: sonnet
description: >
  Visual verification skill — designed for Claude Code UI (desktop/web) where computer use is available. Reads git diff to derive what changed, starts the dev server, navigates to the affected route, and visually tests the golden path + edge cases for the changed components. Gracefully degrades in terminal (prints manual test checklist instead). Czech triggers: "/visual", "zkontroluj vizuálně", "otestuj to vizuálně", "visual check", "podívej se jak to vypadá", or after /implement or /fix when a UI change was made. Does NOT require session context — derives everything from git diff and CLAUDE.md.
---

# /visual — visual verification from diff

Stateless visual tester. Derives everything it needs from `git diff` and `CLAUDE.md` — no session context required. Designed to be called from Claude Code UI (computer use) as an independent reviewer after a terminal session made changes.

**Model**: Sonnet

---

## Step 0 — Ask the user first (MANDATORY)

**Never invoke browser automation automatically.** Before touching the browser, always present both options:

> "Chceš, abych otestoval v browseru (potřebuji tvé schválení), nebo to otestuješ sám?"
> "Should I run the browser test (needs your approval), or will you test it yourself?"

- **User approves** → proceed with full pipeline below.
- **User tests themselves** → skip to [Terminal fallback](#terminal-fallback) and print the manual checklist.

## Environment detection (Step 0b)

After the user approves browser automation, detect whether computer use is available:

**If terminal (no computer use):** skip to [Terminal fallback](#terminal-fallback) at the bottom — print a manual test checklist and exit.

**If UI CC (computer use available):** proceed with full pipeline.

---

## Pipeline

### Step 1 — Read the diff

```bash
git diff main...HEAD --stat        # which files changed
git diff main...HEAD               # full diff for context
```

If no diff from main, fall back to:
```bash
git diff HEAD~1...HEAD             # last commit only
```

From the diff, extract:
- Which **components / pages** changed
- What **behavior** changed (CSS class conditions, event handlers, state logic)
- What **NOT** to test (files unchanged)

### Step 2 — Build test plan

Map changed files to routes and interactions. Derive routes from the diff and CLAUDE.md — do not assume a fixed project structure. For each changed file, infer which page/route renders it.

Example mapping (adapt to the actual project):

| Changed file | Route to open | What to test |
|---|---|---|
| `components/Hero.tsx` | `/` | hero section layout, CTA button |
| `components/ContactForm.tsx` | `/kontakt` | form fields, submit behavior |
| `app/kvetiny/page.tsx` | `/kvetiny` | product listing, images |

Build the actual table from the diff — never use this example table as-is.

Write the test plan before touching the browser:
```
Route: /
Interactions to test:
  1. [specific action] → [expected result]
  2. [specific action] → [expected result]
Edge cases:
  - [what could break]
```

### Step 3 — Start dev server

Read `CLAUDE.md` for the exact dev commands and port. Check if server is already running:

```powershell
# Windows
netstat -ano | findstr :<PORT>
```
```bash
# macOS/Linux
lsof -i :<PORT> | grep LISTEN
```

If not running, start per CLAUDE.md instructions (dev command and port vary per project).

Open browser to the URL specified in CLAUDE.md (e.g. `http://localhost:5173`).

### Step 4 — Execute test plan

For each interaction in the test plan:

1. Navigate to the route
2. Perform the action (tap, swipe gesture, click)
3. Observe the result
4. Compare to expected result from the diff

**For gesture-based interactions** (swipe, drag) on desktop: simulate with mouse drag. Note that touch gestures on desktop may behave differently — flag if unclear.

**Screenshot key states** — before and after each interaction.

**Golden path first, then edge cases.**

### Step 5 — Findings

Classify each finding:

| Type | Description | Action |
|---|---|---|
| ✅ OK | Looks and behaves as expected | Note it, move on |
| 🎨 Visual bug | Wrong color, size, spacing, alignment | Call `/polish` with screenshot as reference |
| 🐛 Functional bug | Wrong behavior, broken interaction, error | Call `/fix` with exact repro steps |
| ❓ Unclear | Can't tell if it's correct without more context | Ask the user |

### Step 6 — Report

```markdown
## Visual verification — [branch name]

**Diff summary:** [2-sentence description of what changed]
**Route tested:** [URL]
**Tested on:** [date]

### Results

- [interaction 1]: ✅ / 🎨 / 🐛 — [description]
- [interaction 2]: ✅ / 🎨 / 🐛 — [description]

### Actions taken
- Called /polish for: [finding] — [what was fixed]
- Called /fix for: [finding] — [what was fixed]
- Follow-up needed: [anything requiring user input]
```

---

## Terminal fallback

When computer use is not available, print a manual test checklist derived from the diff:

```markdown
## Manual visual test checklist

Computer use is not available in this environment. Test the following manually:

**Start dev server:**
cd server && npm run dev
cd client && npm run dev
# Open http://localhost:5173

**Test checklist (derived from diff):**
- [ ] [route]: [specific action] → [expected result]
- [ ] [route]: [specific action] → [expected result]
- [ ] Edge case: [what to verify]

**Report back** what you see and I'll fix any issues.
```

---

## Composability

This skill is designed to be called:
- **Standalone** after `/implement` or `/fix` when UI changes were made
- **From `/implement` T2 pipeline** as an optional visual step before review agent
- **From `/fix`** to verify a visual bug was actually fixed

When calling `/polish` or `/fix` from within this skill, pass the screenshot and exact finding as context — don't make the next skill re-investigate.

---

## Anti-patterns

- Don't test the whole app — only what the diff touched
- Don't flag things that weren't changed as bugs (check the diff first)
- Don't simulate touch gestures and claim mobile was tested — flag it as "desktop only, mobile needs separate verification"
- Don't skip the terminal fallback — a manual checklist is better than silence
