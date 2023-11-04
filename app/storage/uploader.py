import logging
from typing import Dict

from google.api_core.exceptions import Forbidden
from google.cloud import storage
from google.cloud.storage import Blob, Bucket, Client
from starlette import status

from src.settings import app_settings


def upload_file(file_name: str, destination: str | None = None) -> Dict:
    return _upload_to_gcloud(source_file_name=file_name, destination_blob_name=destination)


def _upload_to_gcloud(source_file_name: str, destination_blob_name: str | None = None) -> Dict:
    """
    Uploads a file to the bucket.
    :param source_file_name: The path to your file to upload (ex: "local/path/to/file")
    :param destination_blob_name: The ID of your GCS object (ex: "storage-object-name")
    :return:
    """
    bucket_name = app_settings.BUCKET_NAME

    storage_client: Client = storage.Client()
    bucket: Bucket = storage_client.bucket(bucket_name)
    destination = destination_blob_name if destination_blob_name else source_file_name
    blob: Blob = bucket.blob(destination)

    if blob.exists():
        logging.info(f"File {destination} already exists in bucket {bucket_name}")
        return {"status": status.HTTP_200_OK, "url": blob.public_url}

    try:
        blob.upload_from_filename(source_file_name)
        blob.make_public()
    except Forbidden as e:
        logging.error(e)
        return {"status": status.HTTP_403_FORBIDDEN, "url": ""}

    logging.info("File {} uploaded to {}.".format(source_file_name, destination))
    return {"status": status.HTTP_201_CREATED, "url": blob.public_url}
