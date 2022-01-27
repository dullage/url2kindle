FROM python:3.8-slim-bullseye

ARG USER=url2kindle
ARG UID=1000
ARG GID=1000

ARG APP_DIR=/app

RUN addgroup \
    --gid $GID \
    ${USER} \
    || echo "Group '${GID}' already exists."

RUN adduser \
    --disabled-password \
    --gecos "" \
    --no-create-home \
    --ingroup ${USER} \
    --uid ${UID} \
    ${USER} \
    || echo "User '${UID}' already exists."

RUN apt update && apt install -y \
      npm \
      libmagic1 \
 && rm -rf /var/lib/apt/lists/* \
 && pip install pipenv

WORKDIR ${APP_DIR}

COPY Pipfile Pipfile.lock LICENSE ./
RUN pipenv install --system --deploy --ignore-pipfile
RUN npm install -g @postlight/mercury-parser
COPY main.py url2kindle.py ./

RUN chown -R ${UID}:${GID} ${APP_DIR}
USER ${UID}

ENTRYPOINT [ "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]
