FROM python:3.14-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /srv

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --group prod --no-install-project

COPY . .

RUN uv sync --frozen --no-dev --group prod --no-editable

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uv", "run", "gunicorn", "incubator.wsgi:application", "--bind", "0.0.0.0:8000"]
