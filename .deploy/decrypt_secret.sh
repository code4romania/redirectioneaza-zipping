#!/bin/sh

WORKDIR=${GITHUB_WORKSPACE}

# Decrypt the file
mkdir "${WORKDIR}/creds"

# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt \
    --passphrase="${STORAGE_CREDENTIALS_PASSPHRASE}" \
    --output "${WORKDIR}/creds/storage-credentials.json" \
    "${WORKDIR}/storage-credentials.json.gpg"
