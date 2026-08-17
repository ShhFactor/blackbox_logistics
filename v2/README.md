# Marketplace v2

Django 5.2 LTS foundation for the production marketplace.

This directory is intentionally separate from `marketplace_sim_v1/`. The v1
simulator remains unchanged and is the source material for the logistics work.

## Local setup

```bash
python -m venv .venv
# activate the virtual environment
pip install -r requirements.txt
python manage.py check
python manage.py test
```

The default database configuration expects PostgreSQL. For a complete local
environment:

```bash
docker compose up --build
```

Then visit `/health/`.

Do not commit a real `.env` file or production credentials.
