---
name: sentry
model: sonnet
description: >
  Use when the user wants to check, triage, or fix errors/alerts in Sentry. Czech triggers: "/sentry", "mrkni do sentry", "jsou tam nějaké chyby", "co hlásí sentry", "vyřeš ten alert", "projdi sentry chyby", "ověř ty chyby v sentry", or after a deploy/merge when checking for new errors. Verifies the Sentry MCP is connected, lists unresolved issues, triages each one (real bug / app noise / dev artifact), fixes real bugs in code, proposes a config/ignore filter for noise, and resolves issues in the tracker only with explicit user consent (external write). Do not use for non-Sentry observability tools.
---

# /sentry — triage and fix Sentry alerts

A standardized loop from "are there errors in Sentry?" to a fix or a clean, evidence-backed triage. Stops the ad-hoc poking around the dashboard.

**Model**: Sonnet

**Language**: talk to the user in their language (Czech here); any code/config/commit you produce is English (per the project's CLAUDE.md).

---

## Step 0 — Verify the Sentry MCP is connected

- This skill needs the **Sentry MCP** (tools like `search_issues`, `get_sentry_resource`, and the `search_tools` + `execute_tool` dispatch).
- If no Sentry tool is available: tell the user the Sentry MCP isn't connected and **stop** — offer that they connect it, or paste the error details (title + stacktrace + route). Don't guess.
- **Do not** try to read issues via the build-plugin `SENTRY_AUTH_TOKEN` from `.env.sentry-build-plugin` — that token is for source-map upload and lacks issue-read scope (returns `403`).
- Resolve **org / project** from `next.config.mjs` (`withSentryConfig(..., { org, project })`) or from `find_organizations` / `find_projects`. Note the region (the DSN / token payload carries it, e.g. `de.sentry.io`).

## Step 1 — List unresolved issues

```
search_issues(organizationSlug, projectSlugOrId, query="is:unresolved", sort="date", limit=25)
```

Summarize each: title, culprit, first/last seen, event count, **environment**, **release**.

## Step 2 — Triage each issue into one of three buckets

Pull detail with `get_sentry_resource(url=…)` and classify with evidence (quote the culprit / `mechanism` / a first-party stack frame / the `environment` tag):

1. **Real application bug** — stacktrace in first-party code, reproducible, hits production. → **fix in code**.
2. **App noise** — real-ish but non-actionable: resource-load errors (`target` is an `HTMLElement` / `<link>`), `Non-Error promise rejection captured`, third-party/extension scripts, network blips, bots. → **filter**, don't "fix" code that isn't broken.
3. **Dev artifact** — `environment: development`, transient build errors (`ENOENT .next/…`), HMR, stale cache. → not a real bug. → **gate Sentry to production** or ignore.

Cross-check the **`release`** tag against recent commits: an error on a release *before* your change isn't caused by it. Say so explicitly.

## Step 3 — Act per bucket

- **Real bug:** if you can't pin the root cause from the detail, run `analyze_issue_with_seer(issueUrl=…)` for a code-level analysis + suggested fix. Then implement it (follow the project's CLAUDE.md and verification — `tsc`, build, smoke). If it's bigger than a quick fix, hand it to `/create` as a tiered issue instead of forcing it here.
- **App noise:** propose a **surgical** filter in the Sentry init — `ignoreErrors`, `denyUrls`, or a `beforeSend` that drops non-Error / resource events. Don't blanket-disable.
- **Dev artifact:** the usual fix is `enabled: process.env.NODE_ENV === "production"` in **all three** inits (`instrumentation-client.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`) so dev noise never reaches Sentry.

## Step 4 — Resolve in the tracker (consent required)

- Resolving / ignoring an issue is an **external system write**. **Ask the user explicitly first** — the auto-mode guard will block an unrequested resolve.
- With consent: `execute_tool(name="update_issue", arguments={ organizationSlug, issueId, status: "resolved" })`.
- Without consent: leave it open and either (a) add `Fixes <ISSUE-ID>` to the fix commit (auto-resolves *only if* Sentry's commit/release integration is configured), or (b) give the user the dashboard link to click.

## Step 5 — Ship & summarize

- If you changed code, hand off to `/git`. The **code fix** and the **tracker resolution** are separate — don't claim merging closed the Sentry issue unless integration is wired.
- Summary per issue: bucket + action (fixed / filtered / gated / left open) + what still needs the user (consent to resolve, or a manual dashboard action).

---

## Anti-patterns

- Treating dev-environment noise or resource-load errors as real bugs and "fixing" code that isn't broken.
- Resolving issues in the tracker without explicit user consent.
- Reading issues via the build-plugin auth token (wrong scope → 403) instead of the MCP.
- Blanket-disabling Sentry when only one noise pattern needs filtering — use the narrowest filter that works.
- Reporting "fixed" when you only gated/filtered the noise, or only resolved the ticket without addressing a real bug.
