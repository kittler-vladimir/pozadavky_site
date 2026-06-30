# Tier Routing — detailní kritéria

Jak určit tier issue pokud není explicitně uveden v spec.

---

## Rozhodovací strom

```
Zasahuje to víc než 3 soubory?
├── NE → T1 (pravděpodobně)
└── ANO →
    Potřebuje to architektonické rozhodnutí?
    ├── ANO → T3
    └── NE →
        Jsou tam tvrdé závislosti (migrace → typy → UI)?
        ├── ANO → T2–T3
        └── NE → T2
```

---

## T1 — Signály

- Změna v jednom souboru nebo komponentě
- Jasné řešení, žádné alternativy k zvážení
- Žádná DB migrace
- Žádná nová závislost (npm package)
- Odhad: < 2 hodiny práce

**Příklady:**
- Oprava textu / labelu
- Přidání CSS třídy / style change
- Jednoduchý bug fix v izolované funkci
- Přidání nového sloupce do existující tabulky (bez migrace)
- Drobná UX změna (velikost tlačítka, spacing)

---

## T2 — Signály

- 3–10 souborů
- Nová feature s jasným scope
- Může obsahovat DB migraci
- Potřeba koordinace (BE + FE musí sedět)
- Odhad: 1–3 dny

**Příklady:**
- Nová stránka s formulářem
- CRUD pro novou entitu
- Integrace třetí strany (API key, webhook)
- Refactoring komponenty s zachováním chování
- Přidání auth k existující stránce

---

## T3 — Signály

- 10+ souborů nebo nejasný počet
- Architektonické rozhodnutí (jak to udělat není jasné)
- Cross-cutting concern (zasahuje auth, logging, error handling globálně)
- Breaking change (mění API, schéma, kontrakt)
- Nová doména v aplikaci (první platební flow, první multi-tenant feature)
- Odhad: > 3 dny

**Příklady:**
- Nový modul (reporty, notifikace, platby)
- Migrace DB schématu s datovou transformací
- Implementace RLS / row-level security
- Přechod na nový auth provider
- Multi-tenant architektura

---

## Edge cases

**"Vypadá jako T1, ale..."**
- Pokud změna ovlivňuje shared komponentu používanou na 10 místech → povýšit na T2
- Pokud změna vyžaduje DB migraci → minimálně T2
- Pokud si nejsi jistý scope → T2, ne T1

**"T3 issue lze rozdělit?"**
Pokud T3 issue jde rozdělit na samostatné T1/T2 issues → rozděl. Menší issues = rychlejší feedback loop. Použij `/create` pro každý sub-issue.

**"Tier se změnil v průběhu implementace"**
Pokud při explore fázi zjistíš že scope je větší než tier říkal → zastav, informuj uživatele, dohodněte se jak pokračovat. Nikdy neinplementuj "jen ještě tohle navíc" bez vědomí uživatele.
