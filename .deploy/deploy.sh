#!/bin/bash

set -e

# switch to the directory containing your app.yml (or similar) configuration file
# note that your repository is mounted as a volume to the /deploy directory
WORKDIR=${GITHUB_WORKSPACE}

[ -d "${WORKDIR}/creds" ] || mkdir "${WORKDIR}/creds"
echo "${STORAGE_CREDENTIALS}" > "${WORKDIR}/creds/storage-credentials.json"

cat <<EOT >> "${WORKDIR}/.env"
RUNNING_MODE="${RUNNING_MODE:-background}"
RUN_CLEAN_UP="${RUN_CLEAN_UP:-True}"

GOOGLE_APPLICATION_CREDENTIALS="${WORKDIR}/creds/storage-credentials.json"

BUCKET_NAME="${STORAGE_BUCKET_NAME}"
SECRET_PASSPHRASE="${APPLICATION_PASSPHRASE}"
EOT

docker compose -f docker-compose.build.yml build --no-cache --pull api
docker compose -f docker-compose.build.yml push api
