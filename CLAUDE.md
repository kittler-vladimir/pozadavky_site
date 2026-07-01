# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Pozadavky Site** — Django webová aplikace pro evidenci a sledování požadavků (úkolů), jejich autorů, řešitelů a stavu plnění. Obsahuje i modul **Kniha provozu** pro evidenci skriptů a naplánovaných úloh (kdo je vytvořil, kde běží, jak/jak často se spouští). UI a doménové texty jsou v češtině.

## Jazyk komunikace

Komunikuj s uživatelem v tomto repozitáři **česky** — odpovědi v chatu, otázky, vysvětlení. Anglicky piš pouze to, co je určeno ke sdílení mimo konverzaci nebo pro jiné agenty: GitHub issues, PR title/body, commit messages, kód, komentáře v kódu, instrukce pro subagenty. Češtinu uvnitř anglického textu používej jen v uvozovkách/kódu při citaci konkrétního UI textu nebo doménového pojmu.

## Tech stack

- Python / Django `2.2.28` (old-style, pre-`Field.help_text`-heavy APIs; avoid suggesting Django 3+/4+ only features)
- DB: SQLite lokálně (`db.sqlite3`, via `settings/local.py`), PostgreSQL v produkci (`psycopg2`, viz `settings/base.py`)
- `django_middleware_global_request` — dává přístup k aktuálnímu requestu mimo view (`get_request()`), používá se v `admin.py` k automatickému doplnění `author`
- `xlsxwriter` — export do Excelu
- Nginx + uWSGI v produkci (konfigurace v `conf/`)
- Docker (`Dockerfile`)

## Commands

```bash
pip install -r pozadavky.txt      # install deps (requirements file, despite the .txt extension)
python manage.py runserver        # dev server → http://127.0.0.1:8000/
python manage.py migrate          # apply migrations
python manage.py makemigrations   # after model changes, per-app: makemigrations pozadavky / kniha_provozu
python manage.py createsuperuser
python manage.py test                          # all tests
python manage.py test pozadavky_site.pozadavky      # single app
python manage.py test pozadavky_site.kniha_provozu  # single app
```

There is no linter/formatter config in the repo — don't invent one.

## Architecture

Django project `pozadavky_site` with two apps living **inside** the project package (not siblings of it):

```
pozadavky_site/
├── pozadavky_site/            # project package (settings, root urls) AND parent of both apps
│   ├── pozadavky/             # app: úkoly/požadavky (main task tracker)
│   ├── kniha_provozu/         # app: provozní kniha (registr skriptů/úloh)
│   └── settings/
│       ├── base.py            # shared settings, incl. INSTALLED_APPS, PostgreSQL prod DB config
│       └── local.py           # local override — SQLite, imported after base.py if present
├── templates/                  # project-level template dir (DIRS in TEMPLATES), shared base.html/menu.html
│   ├── kniha_provozu/          # kniha_provozu's own templates
│   └── requirement/            # older/alternate template set for pozadavky (see below)
└── static/
```

Apps are referenced with their full dotted path everywhere: `pozadavky_site.pozadavky`, `pozadavky_site.kniha_provozu` (see `INSTALLED_APPS` in `settings/base.py` and imports in `urls.py`). `manage.py` sets `DJANGO_SETTINGS_MODULE=pozadavky_site.settings`, which resolves to `pozadavky_site/settings/__init__.py` → imports `base` then `local`.

### `pozadavky` app (main task tracker)

- Single model `Requirement` (`models.py`) plus lookup tables `Work_status` and `Requirement_type`. `Requirement.save()` auto-sets `status` to "Splněno"/"Rozpracováno" based on whether `done` is set — this logic is duplicated in `admin.py`'s `save_model` (Django admin bypasses `Model.save()`'s custom fields being touched by the form, so both places recompute status).
- All list views funnel through `render_task_list()` in `views.py`, which applies visibility rules (superuser sees all; staff sees own + own groups; regular users see only their own), then optional `?q=` search, then pagination (33/page), then renders `tasks.html`. Adding a new "filtered task list" view means writing a small view that builds a `filters` dict and delegates to `render_task_list`.
- `views_old.py` and `urls_middelware_example.py` are legacy/reference code, not wired into `urls.py` — don't treat them as active behavior.
- Two overlapping template sets exist: `templates/*.html` (used by current `views.py`, e.g. `tasks.html`, `homepage.html`) and `templates/requirement/*.html` (older set). New work should use the top-level templates unless a task explicitly references the `requirement/` set.
- `RequirementAdminForm` (in `admin.py`) dynamically scopes the `owner` field's queryset to users belonging to the selected `group_owner`, via POST data or the instance — mirrors the AJAX endpoint `get_owners`/`users_by_group` used for the same purpose in the plain-form UI.

### `kniha_provozu` app (script/task catalog)

- Two models: `ZaznamKnihaProvozu` (one entry per registered script/task — `name`, `version`, `author`, `location`, `command`, `launched_at`, `type_of_launch`, `trigger_frequency`, `description`, `link_to_details`, `status`, plus auto-set `created_by`/`added`) and `HistorieKnihaProvozu` (per-field change history, FK'd via `zaznam_id` to the entry with `related_name='Id'` — note the unusual capitalized related name, used as `zaznam.Id.all()` in `views.py`).
- `launched_at` uses an HTML5 `datetime-local` widget; Django 2.2's `DateTimeField.to_python()` has no ISO-8601 parsing shortcut and only tries `DATETIME_INPUT_FORMATS` (space-separated by default), so the form field explicitly declares `input_formats=['%Y-%m-%dT%H:%M', ...]` to accept the browser's `T`-separated value — any other `datetime-local` field added to this project needs the same treatment.
- Change tracking is manual and duplicated in two places: `views.zaznam_update` and `admin.ZaznamKnihaProvozuAdmin.save_model` both diff `TRACKED_FIELDS` against the pre-save object and write `HistorieKnihaProvozu` rows for any field that changed. If `TRACKED_FIELDS` or the model's tracked fields change, update the list in **both** `views.py` and `admin.py`.
- `created_by` ("Vytvořil") is a plain `CharField`, set once at creation from the logged-in user (`request.user.get_full_name() or request.user.username`), never trusted from form input, and excluded from `TRACKED_FIELDS` — unlike the rest of the catalog fields, it's immutable after creation (mirrors "who created this", not "who last touched this").
- `type_of_launch`, `trigger_frequency`, and `status` are `CharField` with `choices=` tuples defined in `models.py` (Czech text used as both DB value and label) — this app has no separate lookup models for these, unlike `pozadavky`'s `Work_status`/`Requirement_type`.
- URLs are namespaced (`app_name = 'kniha_provozu'`, included at `/kniha-provozu/` in the root `urls.py`) — reverse with `kniha_provozu:zaznam_list` etc.
- All views require `@login_required`.

## Things to watch for

- `settings/base.py` has a hardcoded production PostgreSQL host/user/password committed in the repo (overridden locally by `settings/local.py`'s SQLite config, so local dev is unaffected). Don't propagate that pattern to new config; if asked to touch DB settings, flag this to the user rather than silently working around it.
- `Dockerfile` and `conf/` (nginx/uwsgi) still reference an old project name `dp2_site` (paths like `/www/dp2_site`, `dp2_site.ini`) rather than `pozadavky_site` — these are stale and would not build/deploy correctly as-is. Don't assume the Docker setup is verified working.
- `app.spec` (PyInstaller spec for `app.py`) is unrelated leftover — there is no `app.py` in this repo; ignore it.
