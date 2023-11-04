FROM python:3.11.6-slim-bookworm as build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    pip install -U pip


# Python virtualenv paths
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /build
COPY ./requirements.txt .
RUN python3 -m pip install --upgrade pip setuptools && \
    python3 -m pip install -r ./requirements.txt


FROM python:3.11.6-slim-bookworm

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get upgrade -y && \
    pip install -U pip


# Python virtualenv paths
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app

# copy the source code and build artifacts
COPY ./app ./
COPY --from=build "${VIRTUAL_ENV}" "${VIRTUAL_ENV}"

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

# activate the virtualenv:
RUN . "${VIRTUAL_ENV}/bin/activate"

ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 80
