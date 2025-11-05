#!/bin/bash
REGION="us-central1"
PROJECT_ID="hw5-20187363"


# This makes sure that we are uploading our code from the proper path.
# Don't change this line.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

REPO_NAME="hw5-images"
REGISTRY="us-central1-docker.pkg.dev"
APP_IMAGE="frontend_v1"
TARGET_DOCKERFILE="Dockerfile.${APP_IMAGE}"
SERVING_PORT=8000

# It's not expected to know bash scripting to the level below.
# The following is known as substitutions in cloud build.

REPO_URI="${REGISTRY}/${PROJECT_ID}/${REPO_NAME}"
gcloud builds submit \
    --region=${REGION} \
    --config="${SCRIPT_DIR}/cloudbuild.yaml" \
    --substitutions=_BASE_IMAGE_URI="${REPO_URI}/base_image",_APP_URI="${REPO_URI}/${APP_IMAGE}",_SERVING_PORT=${SERVING_PORT},_TARGET_DOCKERFILE="${TARGET_DOCKERFILE}" \
    "${SCRIPT_DIR}/../"
