---
name: insights
model: sonnet
description: >
  Use when the user wants to improve their workflow or find out what to do differently next time. Czech triggers: "/insights", "co zlepšit", "jak si vedu", "přehled workflow", "co se opakuje", "vylepši skilly", or run monthly as a routine. Reads session history, identifies patterns, proposes concrete improvements — new rules for CLAUDE.md, skill edits, new agent prompts. This is the meta-loop that makes the whole stack self-improving.
---

# /insights — workflow improves itself

Meta-loop for continuous improvement. Reads session history, finds patterns, proposes concrete actions.

**Model**: Sonnet

**Run**: monthly, or whenever something feels broken.

---

## Step 1 — Load history

Use these tools to load sessions for the recent period:

```
mcp__ccd_session_mgmt__list_sessions(limit=20)
```

To search for specific patterns across sessions (recurring errors, specific topics):

```
mcp__ccd_session_mgmt__search_session_transcripts(query="...", limit=20)
```

Example useful queries: `"TypeScript error"`, `"migration"`, `"fixed"`, `"manually"`.

Look for in the history:
- Sessions where something repeated multiple times
- Moments where you fixed the same error
- Places where you had to intervene manually instead of the agent
- Tasks that took longer than they should have
- Things that worked well and why

---

## Step 2 — Pattern analysis

Identify patterns in these categories:

### Recurring errors
> "What did I fix more than once?" → belongs in CLAUDE.md

Example signals:
- The same type of TypeScript error repeated
- Agent forgot to run migration
- Incorrect import path kept recurring
- Missing `"use client"` or unnecessary ones

### Unnecessary manual work
> "What did I do by hand that an agent could have done?" → new skill or extension of existing one

Example signals:
- Manually written commit messages every time in the same format
- Manually copying data between files
- Repeating setup steps

### Scope creep
> "Where did the project balloon?" → tighten Out of Scope in discovery/create

Example signals:
- Feature added "just one more thing"
- Issue took 3× longer than tier said
- New dependency appeared mid-implementation

### What worked well
> "What to repeat?" → solidify as a rule or pattern

---

## Step 3 — Improvement proposals

For each pattern found, propose a concrete action:

### Proposal format

```markdown
## Pattern: [name]

**Observation**: [what repeats, how often]

**Impact**: [what it costs — time, errors, frustration]

**Proposed action**:
- Type: [CLAUDE.md rule / skill edit / new skill / discovery change]
- Specifically: [exactly what to change or add]
- Priority: [high / medium / low]
```

---

## Step 4 — Action plan

Sort proposals by priority and offer the user a choice:

```markdown
## Action plan

### Immediately (high priority)
1. [action] → [where to change it]
2. ...

### This week (medium priority)
1. [action] → [where to change it]

### Next time (low priority / consider)
1. [action] → [where to change it]
```

Ask: *"Do you want to go through each item and implement them right now?"*

---

## Step 5 — Implement changes

If the user agrees, make the changes:

**CLAUDE.md rule** → open CLAUDE.md, add to the right section, explain why

**Skill edit** → identify which skill to update, propose specific text changes

**New skill** → if the pattern is large enough → run skill-creator workflow

**Discovery/create change** → update tier criteria or intake questions

---

## Step 6 — Update Notion documentation

**Always** after any insights run where something changed, update the Notion stack page.

Page: https://app.notion.com/p/3765cb1530a68113a8c6f7f4822be551

What to update:

**Changelog** — add a row to the table:
```
| YYYY-MM-DD | [brief description of what changed] |
```

**Page content** — if a skill changed, a new feature was added, or the workflow changed:
- Update the relevant section (When to use what, Flow, Tips...)
- Add a new skill to the install table if one was added
- Remove or rewrite outdated information

**What NOT to update**:
- Internal implementation details of skills (those live in `.skill` files)
- Technical agent prompts
- The page should remain a concise guide for users, not technical documentation

If changes are small (just a CLAUDE.md rule), a changelog row is enough.
If a new skill was added or an entire flow changed, update the relevant sections too.

---

## Output

At the end of each insights run, generate a brief summary:

```markdown
## /insights summary — [date]

**Sessions analyzed**: [N]
**Patterns found**: [N]

**Changes made**:
- [what was changed]

**Deferred to next time**:
- [what was identified but not implemented]

**Overall workflow health**: [1–10] — [one-sentence justification]
```

---

## Routine

Recommended frequency:
- **Monthly**: full insights run (20+ sessions)
- **After a large project**: short run (5–10 sessions) — what to learn from this project?
- **When frustrated**: whenever the workflow feels broken
