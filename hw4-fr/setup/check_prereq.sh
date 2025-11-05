#!/bin/bash

# Get user input for student ID
read -p "Enter your student ID: " student_id

# Strip leading and trailing whitespace from student ID
student_id=$(echo "$student_id" | sed 's/^[ \t]*//;s/[ \t]*$//')

# Check if gcloud is installed
echo "Checking if gcloud is installed..."
if ! command -v gcloud &> /dev/null; then
    echo "gcloud is not installed. Please install gcloud before running this script."
    exit 1
fi

# Check that the project is set to hw5-${student_id}
PROJECT_ID="hw5-${student_id}"
PROJECT_REGION="us-central1"

echo "Checking if the project is set to ${PROJECT_ID}..."
project_name=$(gcloud config get-value project)
if [ "$project_name" != "${PROJECT_ID}" ]; then
    echo "Project is not set to ${PROJECT_ID}. Please set the project to ${PROJECT_ID} before running this script."
    exit 1
fi

# Check that the following services are enabled:
# - Cloud Run
# - Artifact Registry
# - Cloud Build
echo "Checking if Cloud Run is enabled..."
gcloud services list --enabled --format="value(config.name)" | grep -q "run.googleapis.com"
if [ $? -ne 0 ]; then
    echo "Cloud Run is not enabled. Please enable Cloud Run before running this script."
    exit 1
fi

echo "Checking if Cloud Build is enabled..."
gcloud services list --enabled --format="value(config.name)" | grep -q "cloudbuild.googleapis.com"
if [ $? -ne 0 ]; then
    echo "Cloud Build is not enabled. Please enable Cloud Build before running this script."
    exit 1
fi

echo "Checking if Artifact Registry is enabled..."
gcloud services list --enabled --format="value(config.name)" | grep -q "artifactregistry.googleapis.com"
if [ $? -ne 0 ]; then
    echo "Artifact Registry is not enabled. Please enable Artifact Registry before running this script."
    exit 1
fi

# Check that a Docker registry exists with the following setup:
# - Location: us-central1
# - Repository: hw5-images
REPO_NAME="hw5-images"
REPO_PATH="${PROJECT_REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}"
echo "Checking if a Docker registry exists with the following setup:"
echo " - Location: ${PROJECT_REGION}"
echo " - Repository: ${REPO_NAME}"

if gcloud artifacts repositories describe "${REPO_NAME}" \
    --project="${PROJECT_ID}" \
    --location="${PROJECT_REGION}" &> /dev/null
then
    echo "Repository ${REPO_PATH} exists"
else
    echo "Repository ${REPO_PATH} does not exist"
    exit 1
fi

# Check that the autograder service account has read access to the Docker registry
# The autograder service account will be from the TA GCP account.
# The service account is: ta-autograder@ift6758-hw5-gcp-24.iam.gserviceaccount.com
# TEST ACCOUNT: ift6758-ta-hw5-gcp-autograder@hw5-12345.iam.gserviceaccount.com
TA_SERVICE_ACCOUNT="ift6758-ta-hw5-gcp-autograder@hw5-12345.iam.gserviceaccount.com"
iam_policy=$(gcloud artifacts repositories get-iam-policy "${REPO_NAME}" \
    --project="${PROJECT_ID}" \
    --location="${PROJECT_REGION}" \
    --format="yaml")

# Check python is installed and has yaml package
echo "Checking if python is installed..."
if ! command -v python &> /dev/null; then
    echo "Python may not be installed. Please double check your Python installation before running this script."
fi

echo "Checking if python has yaml package..."
if ! python -c "import yaml" &> /dev/null; then
    echo "Python does not have the yaml package. Please install the yaml package (pyyaml) before running this script."
    exit 1
fi

# Everything probably worked, so we can exit with a success message and status.
echo "All prerequisites are met. You can proceed with the assignment."
exit 0
