---
name: continue
description: >
  Použij tento skill vždy, když uživatel chce pokračovat v přerušené T3 implementaci — po kompakci kontextu, po limitu tokenů, nebo po restartu session. Triggery: "/continue", "pokračuj", "kde jsme skončili", "dojel limit", "resume implementaci", "navař dál", nebo když je v projektu soubor `.claude/implement-state.md`. Skill načte checkpoint, zjistí kde pipeline skončil a pokračuje od správného kroku.
---

# /continue — resume přerušené implementace

Načte checkpoint z `.claude/implement-state.md` a pokračuje v T3 pipeline od místa přerušení.

**Model**: Sonnet

---

## Krok 1 — Detekce tier a stavu

Spusť paralelně:
```bash
git branch --show-current
git status --short
git diff --stat HEAD
```

Pak zkontroluj zda existuje `.claude/implement-state.md`.

### Větev A — state soubor existuje (T2 nebo T3)

Přečti soubor, zjisti `**Tier**`. Pokračuj na Krok 2.

### Větev B — state soubor neexistuje (T1 nebo ztracený checkpoint)

Rekonstruuj stav z gitu:

1. `git log --oneline -5` — kolik commitů přibylo od začátku práce?
2. `git diff HEAD` — jsou neuložené změny?
3. Zeptej se jednou otázkou:

> „Nevidím checkpoint. Jaký tier a krok jsme přerušili?"
> - T1: Explore / Implement / Review / Shrnutí
> - T2: Explore / Plan / Implement / Verifikace / Code review / Final build / Shrnutí
> - T3: uveď číslo kroku (01–11)

Na základě odpovědi + git diff odhadni co je hotovo a pokračuj na Krok 3.

---

## Krok 2 — Orientace ve stavu (T2 / T3)

Ze state souboru zjisti:

- **Issue**: číslo a název
- **Tier**: T2 nebo T3
- **Branch**: ověř `git branch --show-current` — musí sedět se souborem
- **Poslední dokončený krok**: hledáš poslední `[x]` v seznamu kroků
- **T3 navíc**: přečti "Výstupy dokončených kroků" a "Otevřené nálezy z review"

Vypiš uživateli shrnutí:

```
Nalezen checkpoint (Tier X) — Issue #N: [název]
Dokončeno: kroky 01–[N]
Pokračuji od: krok [N+1] — [název kroku]
Branch: [branch]
```

---

## Krok 3 — Resume pipeline

Pokračuj od dalšího nedokončeného kroku podle tieru:

### T1 (4 kroky)
```
1. Explore      → přečti dotčené soubory (max 5)
2. Implement    → napiš kód, verifikuj (tsc)
3. Review       → zkontroluj diff
4. Shrnutí      → jak otestovat, co bylo změněno
```

### T2 (7 kroků)
```
01. Explore         → přečti dotčené soubory (max 10)
02. Plan            → implementační plán
03. Implement       → sekvenční implementace
04. Verifikace      → tsc + build + testy
05. Code review     → skill code-review
06. Final build     → čistý build
07. Shrnutí         → jak otestovat → /git
```

### T3 (11 kroků)
```
01. Explore              → přečti dotčené soubory
02. Analyze              → závislosti, rizika
03. Plan                 → implementační plán
04. Impl. fáze 1 (‖)     → BE: migrace, typy, schéma | FE: skeleton
05. Verifikace fáze 1    → tsc + migrace
06. Impl. fáze 2 (‖)     → BE: API routes | FE: UI + logika
07. Verifikace fáze 2    → tsc + build + testy
08. Writer/Reviewer      → code review v čistém kontextu
09. Testy + docs         → test-engineer + documentation-writer
10. Final build          → čistý build, všechny testy projdou
11. Shrnutí              → co bylo změněno, jak otestovat → /git
```

Po každém dokončeném kroku **aktualizuj checkpoint** (přepiš `[ ]` na `[x]`, T3 doplň výstup sekce).

---

## Krok 4 — Po dokončení

Po kroku 11 (Shrnutí):
- Smaž `.claude/implement-state.md`
- Nabídni přechod na `/git`

```bash
rm .claude/implement-state.md
```

---

## Edge cases

**Branch nesedí** (lokální branch ≠ state soubor):
→ Zastav, informuj uživatele. Pravděpodobně špatný projekt nebo stará state.

**State soubor je poškozený / nečitelný**:
→ Zkus rekonstruovat z `git log` a `git diff`. Zeptej se uživatele na potvrzení.

**Kompakce proběhla uprostřed fáze** (krok označen jako `[x]` ale práce není v kódu):
→ Přečti `git diff` od začátku branch. Pokud krok skutečně chybí, opakuj ho.
