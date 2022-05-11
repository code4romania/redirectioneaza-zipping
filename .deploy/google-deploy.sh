#!/bin/bash

# Authenticate with the Google Services
codeship_google authenticate

# switch to the directory containing your app.yml (or similar) configuration file
# note that your repository is mounted as a volume to the /deploy directory
WORKDIR=${GITHUB_WORKSPACE}

# deploy the application
gcloud compute copy-files "${WORKDIR}/app" "${INSTANCE_NAME}:${REMOTE_PATH}"
