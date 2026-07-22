FROM python:3.13.9-alpine3.22


ARG USERNAME=carapi
SHELL ["/bin/ash", "-o", "pipefail", "-c"]
ENV POETRY_VERSION=2.4.0 \
    PATH="/home/${USERNAME}/.local/bin:$PATH"


RUN apk add curl=8.14.1-r3 \
    --no-cache && \
    rm -rf /var/cache/apk/* && \
    adduser -s /bin/bash -D ${USERNAME}

USER ${USERNAME}

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /home/${USERNAME}

COPY --chown=user:${USERNAME} pyproject.toml poetry.lock ./
RUN poetry install \
    --without dev \
    --no-root \
    --no-ansi

COPY --chown=user:${USERNAME} . .

CMD [ "poetry", "run", "fastapi", "dev", "car_api/app.py", "--host", "0.0.0.0" ]