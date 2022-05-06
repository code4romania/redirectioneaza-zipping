#!/bin/bash

if [[ ${ENVIRONMENT} != "production" ]] ; then
    uvicorn main:app --host 0.0.0.0 --port 80 --reload
else
    uvicorn main:app --host 0.0.0.0 --port 80
fi
