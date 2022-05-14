#!/bin/bash

if [[ ${ENVIRONMENT} != "production" ]] ; then
    uvicorn main:app --host 0.0.0.0 --port 80 --reload
else
    CREDENTIALS_DIRECTORY=$(dirname "${GOOGLE_APPLICATION_CREDENTIALS}")

    [ -d "${CREDENTIALS_DIRECTORY}" ] || mkdir -p "${CREDENTIALS_DIRECTORY}"
    touch "${GOOGLE_APPLICATION_CREDENTIALS}"

    echo "${GOOGLE_CREDENTIALS}" > "${GOOGLE_APPLICATION_CREDENTIALS}"

    uvicorn main:app --host 0.0.0.0 --port 80
fi
