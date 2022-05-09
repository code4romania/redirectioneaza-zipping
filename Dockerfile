FROM python:3.10-slim

ARG ENVIRONMENT
ENV ENVIRONMENT ${ENVIRONMENT:-production}

RUN apt update && pip install -U pip

WORKDIR /code

COPY ./requirements.txt ./requirements-dev.txt /code/

RUN if [ "${ENVIRONMENT}" = "production" ]; \
    then pip install --no-cache-dir --upgrade -r requirements.txt; \
    else pip install --no-cache-dir --upgrade -r requirements-dev.txt; \
  fi

WORKDIR /code/app
COPY ./app /code/app

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 80
