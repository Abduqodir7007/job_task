# Copilot instructions

## Project shape

- Django project scaffold named `config`.
- `manage.py` is the entry point.
- Project settings, ASGI, WSGI, and root URLs live under `config/`.
- PostgreSQL is configured through `DATABASE_URL` in `.env` via `django-environ`.
- Django REST Framework is installed and should be registered in `config/settings.py` when building API features.
- JWT auth is used via `djangorestframework-simplejwt`.
- The project uses a custom user model at `users.User`; keep `AUTH_USER_MODEL` set accordingly.

## Commands

- Install and sync dependencies: `uv sync`
- Fill `.env` before running the project; settings read `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `DATABASE_URL`.
- Run the Django system check: `uv run python manage.py check`
- Create migrations: `uv run python manage.py makemigrations`
- Apply migrations: `uv run python manage.py migrate`
- Run the development server: `uv run python manage.py runserver`
- Run the full Django test suite: `uv run python manage.py test`
- Run a single test case or method: `uv run python manage.py test path.to.TestCaseName`

## Conventions

- Keep app registration in `INSTALLED_APPS` inside `config/settings.py`.
- Keep the auth swap centralized in `config/settings.py` and `users/models.py`; do not reintroduce Django's default `User`.
- Keep API routes under `/api/` through `config/urls.py` includes.
- Keep database settings in `config/settings.py` tied to `DATABASE_URL` rather than hardcoded engine credentials.
- Add new URL routes in `config/urls.py`; keep project-level routing thin and delegate feature URLs to app modules.
- Use Django/DRF defaults unless the project adds explicit settings for serializers, auth, pagination, or API versioning.
- Keep `uv.lock` in sync with `pyproject.toml` when dependencies change.
