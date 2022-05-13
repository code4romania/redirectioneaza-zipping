#!/bin/bash

if [[ ${ENVIRONMENT} != "production" ]] ; then
    uvicorn main:app --host 0.0.0.0 --port 80 --reload
else
    [ -d "/creds" ] || mkdir "/creds"
    echo "${GOOGLE_CREDENTIALS}" > "${GOOGLE_APPLICATION_CREDENTIALS}"

    uvicorn main:app --host 0.0.0.0 --port 80
fi
