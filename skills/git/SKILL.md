---
name: git
model: haiku
description: >
  Use when the user wants to commit, push, create a PR, or merge a branch. Czech triggers: "/git", "commitni to", "pushni", "vytvoř PR", "mergni", "quick ship", or when /implement finishes and offers the handoff to /git. Runs the complete pipeline: commit → push → PR → CI watch → merge → release log. Detects hosting and adapts (local without CI, Vercel preview, GitHub Actions, custom server). Model Haiku — fast and cheap.
---

# /git — quick ship

Complete pipeline from finished code to production. One command, done.

**Model**: Haiku (fast, cheap — this is mechanical work)

---

## Workflow — exactly in this order

### Step 0 — DB backup (optional)

If a `backup-db.ps1` script exists in the project root, run it before anything else:

```powershell
if (Test-Path ".\backup-db.ps1") { .\backup-db.ps1 }
```

If the script doesn't exist, skip silently. If it exists but fails (e.g. Google Drive not mounted), inform the user and ask whether to continue or abort.

If no backup script exists in the project, consider asking the user: *"This project has no DB backup script. Do you want to set one up before we ship?"*

### Step 1 — Status check

```bash
git status
git diff --stat
```

Verify:
- We're on a feature branch (not `main`/`master`)
- Changes are as expected — nothing extra, nothing missing
- Build passed (if not yet, run verification from CLAUDE.md)

If on `main` → stop, ask the user.

### Step 2 — Commit

```bash
git add -A
git commit -m "type(scope): description (Closes #N)"
```

> **Staging guard.** `git add -A` is the default, but first check `git status`. If the repo tracks a **data/DB file that shows as modified** (e.g. `prisma/dev.db`) or there's other unrelated churn, do **not** `git add -A` — stage code/migrations explicitly (`git add src prisma/schema.prisma prisma/migrations …`) and leave the data file out. Follow the project's CLAUDE.md if it has a rule about this.

**Commit message format** (Conventional Commits):

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Refactoring without behavior change |
| `chore` | Maintenance, dependencies, configuration |
| `docs` | Documentation |
| `test` | Tests |
| `style` | Formatting, whitespace (not CSS) |

Rules:
- `scope` = area (e.g. `auth`, `payments`, `dashboard`)
- Description in English — consistently within the project
- `Closes #N` always when an issue exists
- Max 72 characters total

### Step 3 — Push + PR

```bash
git push origin HEAD
gh pr create \
  --title "type(scope): description" \
  --body-file .claude/PR_BODY.md \
  --draft
```

**PR body** — generate from issue and diff, save to `.claude/PR_BODY.md`:

```markdown
## Description
[what was implemented — 2–3 sentences]

## Changes
- [file or area]: [what and why]

## How to test
1. [specific step]
2. [what to verify]

## Issue
Closes #[N]
```

Note: always `--body-file`, never `--body` inline — special characters break the command.

**Language:** the PR title and body are written entirely in **English** (same as commit messages). Use Czech only inside quotes/code when citing an actual UI string or legal/domain term.

### Step 4 — CI watch

Detect hosting and adapt:

**GitHub Actions (general):**
```bash
gh pr checks --watch --fail-fast
```

**Vercel preview:**
```bash
gh pr checks --watch --fail-fast
# Vercel automatically creates a preview deploy — check URL in PR
```

**Local / no CI:**
```bash
# Skip CI watch — nothing to wait for
# Verify manually: npm run build && npm test
```

**Custom server (NAS, Railway):**
```bash
gh pr checks --watch --fail-fast
# or verify deployment log manually
```

**If CI fails:**
1. Read the error
2. If clear → fix, commit, push (`git commit -m "fix: ..."`)
3. If unclear → stop, inform the user
4. Max 1 autofix attempt — then escalate

### Step 5 — Merge

After green CI.

**Auto-merge when CI is clean.** If all checks pass without failures, proceed to squash-merge immediately — no need to ask for permission. Only stop and ask the user if: CI failed, there are open review comments on the PR, or the user has previously indicated they prefer to merge manually.

```bash
gh pr merge --squash --delete-branch
git checkout main
git pull origin main
git remote prune origin   # delete-branch leaves stale local origin/* refs — prune them
```

Squash merge always — clean history, one commit per feature.

**Always prune after merge.** `gh pr merge --delete-branch` removes the remote and local branch but leaves the local remote-tracking ref (`refs/remotes/origin/<branch>`) behind, so the merged branch keeps showing in the user's git graph as "uncleaned". Run `git remote prune origin` (or `git fetch --prune`) right after the pull so no stale branches linger. Verify with `git branch -a` — only `main` and active branches should remain.

### Step 6 — Release log

Generate 3 user-friendly titles for changelog/release notes:

**Rules:**
- Write for users, not developers
- No technical jargon (no "refactoring", "migration", "API")
- Concrete benefit, not implementation description
- In English

**Examples:**
- ✗ `feat(reports): implement new overview with aggregations`
- ✓ `You can now see trends over time in the reports overview`

- ✗ `fix(auth): fix RLS policy for multi-tenant`
- ✓ `Fixed: other users' data was not visible`

Offer 3 variants; the user picks or edits.

---

## Shortcuts

**If everything is in order and the user wants a quick ship:**

```bash
# Entire pipeline in one block
git add -A
git commit -m "feat(scope): description (Closes #N)"
git push origin HEAD
gh pr create --title "..." --body-file .claude/PR_BODY.md
gh pr checks --watch --fail-fast
gh pr merge --squash --delete-branch
git checkout main && git pull
git remote prune origin   # clean up stale local origin/* refs left by --delete-branch
```

**If they only want a commit (no PR):**
```bash
git add -A
git commit -m "type(scope): description"
```

---

## Output

After completion, print:

```
✅ Quick ship complete!

  Commit  ✓  [hash]
  PR      ✓  #[N] — [URL]
  CI      ✓  [or "skipped — local project"]
  Merge   ✓  squash + branch deleted + pruned

Release log (pick or edit):
  1. [variant 1]
  2. [variant 2]
  3. [variant 3]
```

**After shipping — session hygiene.** A shipped PR usually ends a unit of work. If the user's next task is unrelated, suggest `/clear` to start with a fresh context (long sessions stay expensive even when cached). Don't force it — just offer it once.

---

## Anti-patterns

- NEVER `git push --force` on `main`
- NEVER `--body` inline for complex PR text — always `--body-file`
- NEVER merge without green CI (if CI exists)
- NEVER `git add -A` when the repo tracks a data/DB file that shows as modified (e.g. `prisma/dev.db`) — stage code/migrations explicitly so data churn isn't committed
- DON'T commit on behalf of the user without their knowledge — always show what will be committed
