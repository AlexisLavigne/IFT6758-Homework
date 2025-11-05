#!/bin/bash
REGION="us-central1"
PROJECT_ID="hw5-20187363"
REPO_NAME="hw5-images"
REGISTRY="us-central1-docker.pkg.dev"

# This is the service you will be deploying.
# Call this backendv1, backendv2, frontendv1, or frontendv2
SERVICE_NAME="frontendv2"
BUILD_ID="1e92fb79-4350-4c9c-adfa-42004655ceb3"
BACKEND_URL="https://backendv2-627969713837.us-central1.run.app"

# Put your image URI here corresponding to the service above.
# An IMAGE URI has the following format:
# REGION-docker.pkg.dev/PROJECT_ID/REPO_NAME/IMAGE_NAME:TAG
IMAGE_URI="${REGISTRY}/${PROJECT_ID}/${REPO_NAME}/frontend_v2:${BUILD_ID}"

# This should be the same port as the one used when building the image.
SERVING_PORT="8000"

# NOTE: Default values are set for memory and cpu
# but you may need to change these.

gcloud run deploy ${SERVICE_NAME} \
    --region=${REGION} \
    --image=${IMAGE_URI} \
    --min-instances=1 \
    --max-instances=1 \
    --memory="4Gi" \
    --cpu=2 \
    --port=${SERVING_PORT} \
    --allow-unauthenticated \
    --set-env-vars="KEY=VALUE" \
    --set-env-vars="KEY2=VALUE2" \
    --set-env-vars="SERVING_URL=${BACKEND_URL}"

# NOTE: In a production environment, we may not want
# to allow anyone to access our service(s). For the
# purposes of this assignment, it is fine to have
# it public facing.

