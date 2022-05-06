#!/bin/bash

if [[ ${ENVIRONMENT} != "production" ]] ; then
    uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
else
    uvicorn app.main:app --host 0.0.0.0 --port 80
fi
