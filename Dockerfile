FROM python:3.11.4-slim-bookworm AS prod
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.2

# Configuring poetry
RUN poetry config virtualenvs.create false
RUN poetry config cache-dir /tmp/poetry_cache

# Copying requirements of a project
COPY pyproject.toml poetry.lock /apps/
WORKDIR /apps

# Installing requirements
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main
RUN apt-get purge -y gcc && rm -rf /var/lib/apt/lists/*

# Copying actual application
COPY . /apps/
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

CMD ["/usr/local/bin/python", "-m", "apps"]

FROM prod AS dev

RUN --mount=type=cache,target=/tmp/poetry_cache poetry install
