# Pozadavky Site

Django webová aplikace pro evidenci a sledování požadavků (tasků), jejich autorů, řešitelů a stavu plnění. Součástí je i modul **kniha_provozu**.

## Funkce

- Evidence požadavků (úkolů) s detailem, autorem a vlastníkem
- Filtrování úkolů: všechny, splněné, nesplněné, podle uživatele, podle skupiny
- Správa skupin a autorů
- Přihlašování / odhlašování uživatelů (Django auth)
- Administrace přes Django Admin
- Modul **Kniha provozu** (provozní kniha) – viz sekce níže

### Kniha provozu

Modul pro evidenci skriptů a naplánovaných úloh (registr skriptů). Dostupný jak přes vlastní webové stránky (`/kniha-provozu/`), tak přes Django Admin.

**Pole záznamu:**

| Pole | Popis | Povinné? |
|---|---|---|
| Název | Název skriptu/úlohy | Ano |
| Verze | Verze skriptu (volný text) | Ne |
| Autor | Autor skriptu | Ano |
| Místo (adresář) | Adresář, kde se skript nachází | Ano |
| Příkaz | Příkaz, kterým se skript spouští | Ano |
| Spuštěno | Datum a čas spuštění | Ne |
| Typ spuštění | Manuálně / Naplánovaně (cron) / Při události | Ano |
| Frekvence spuštění | Jednorázově / Denně / Týdně / Měsíčně / Ročně / Jinak | Ano |
| Popis | Volný popis | Ne |
| Odkaz na detaily | Odkaz na externí dokumentaci | Ne |
| Stav | Aktivní / Neaktivní / Ukončené / Zastavené / Zastaralé | Ano |
| Vytvořil | Kdo záznam vytvořil – vyplňuje se **automaticky podle přihlášeného uživatele**, neměnné po vytvoření | Ano (auto) |
| Datum publikace | Vyplňuje se automaticky při vytvoření | Ano (auto) |

**Funkce:**
- Dostupné z hlavního menu (odkaz "Kniha provozu", viditelný pro přihlášené uživatele)
- Seznam záznamů zobrazující všechna pole, s vyhledáváním v názvu, autorovi, popisu a příkazu
- Detail záznamu
- Vytvoření a úprava záznamu (přes vlastní formulář i přes Django Admin)
- **Automatická historie změn** – při každé úpravě záznamu se zaznamená, které pole se změnilo, jaká byla původní a nová hodnota, a kdo změnu provedl

**URL:**
- `/kniha-provozu/` – seznam záznamů
- `/kniha-provozu/novy/` – vytvoření nového záznamu
- `/kniha-provozu/<id>/` – detail záznamu (včetně historie změn)
- `/kniha-provozu/<id>/upravit/` – úprava záznamu

## Technologie

- Python / Django `2.2.28`
- SQLite (výchozí databáze pro vývoj)
- `psycopg2` (PostgreSQL adaptér, pro produkční nasazení)
- `xlsxwriter` (export do Excelu)
- `django_middleware_global_request`
- Nginx + uWSGI (konfigurace v `conf/`)
- Docker (`Dockerfile`)

## Instalace a spuštění (lokálně)

1. **Naklonujte repozitář:**
   ```bash
   git clone https://github.com/kittler-vladimir/pozadavky_site.git
   cd pozadavky_site
   ```

2. **Vytvořte a aktivujte virtuální prostředí:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Nainstalujte závislosti:**
   ```bash
   pip install -r pozadavky.txt
   ```

4. **Spusťte migrace databáze:**
   ```bash
   python manage.py migrate
   ```

5. **Vytvořte administrátorský účet:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Spusťte vývojový server:**
   ```bash
   python manage.py runserver
   ```

   Aplikace poběží na `http://127.0.0.1:8000/`.

## Spuštění přes Docker

Projekt obsahuje `Dockerfile` pro snadné nasazení:

```bash
docker build -t pozadavky_site .
docker run -p 8000:8000 pozadavky_site
```

Konfigurace pro Nginx a uWSGI najdete ve složce `conf/`.

## Struktura projektu

```
pozadavky_site/
├── pozadavky_site/        # Hlavní Django projekt
│   ├── pozadavky/         # Aplikace - evidence požadavků/úkolů
│   ├── kniha_provozu/     # Aplikace - provozní kniha
│   ├── settings/          # Nastavení (base.py, local.py)
│   ├── urls.py            # Routování URL
│   └── wsgi.py
├── templates/             # HTML šablony
├── static/                # CSS, JS, obrázky
├── conf/                  # Konfigurace Nginx a uWSGI
├── manage.py
├── pozadavky.txt          # Závislosti (requirements)
└── Dockerfile
```

## Nastavení prostředí

Projekt používá rozdělené nastavení v `pozadavky_site/settings/`:
- `base.py` – základní/sdílené nastavení
- `local.py` – lokální nastavení (databáze, debug, secret key)

Pro produkční nasazení doporučujeme upravit `local.py` (nebo vytvořit `production.py`) a nepoužívat výchozí SQLite databázi, ale PostgreSQL (díky podpoře `psycopg2`).

## Licence

Tento projekt nemá v současné době definovanou licenci.
