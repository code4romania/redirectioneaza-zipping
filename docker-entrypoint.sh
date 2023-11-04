#!/bin/bash

if [[ ${ENVIRONMENT} == "production" || ${CREDENTIALS_SOURCE} == "env_var" ]] ; then
    CREDENTIALS_DIRECTORY=$(dirname "${GOOGLE_APPLICATION_CREDENTIALS}")

    [ -d "${CREDENTIALS_DIRECTORY}" ] || mkdir -p "${CREDENTIALS_DIRECTORY}"
    touch "${GOOGLE_APPLICATION_CREDENTIALS}"

    echo "${GOOGLE_CREDENTIALS}" > "${GOOGLE_APPLICATION_CREDENTIALS}"
fi

if [[ ${ENVIRONMENT} != "production" ]] ; then
    OPTION="--reload"
fi

uvicorn main:app --host 0.0.0.0 --port 80 "${OPTION}"
