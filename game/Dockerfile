FROM python:3.11-slim AS builder

ENV POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    SDL_AUDIODRIVER=dummy

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        libasound2 \
        libegl1 \
        libgl1 \
        libglib2.0-0 \
        libgles2 \
        libx11-6 \
        libxcursor1 \
        libxi6 \
        libxinerama1 \
        libxrandr2 \
        xauth \
        xvfb

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .
RUN poetry install
RUN xvfb-run -a sh ./scripts/build-web.sh

FROM python:3.11-slim AS runtime

WORKDIR /srv/mendels-greenhouse
COPY --from=builder /app/dist/web ./

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health.html', timeout=2).read()"

CMD ["python", "-m", "http.server", "8080", "--bind", "0.0.0.0"]
