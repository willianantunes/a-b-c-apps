FROM python:3.13-slim

WORKDIR /app

RUN useradd appuser && chown appuser ./

RUN pip install --upgrade pip && \
    pip install poetry

COPY --chown=appuser poetry.lock pyproject.toml ./

RUN poetry export -f requirements.txt -o requirements.txt --with-credentials && \
    pip uninstall --yes poetry && \
    pip install --require-hashes -r requirements.txt

COPY --chown=appuser . ./

EXPOSE 8080

USER appuser
