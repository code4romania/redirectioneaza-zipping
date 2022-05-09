import logging
from typing import Dict

from google.api_core.exceptions import Forbidden
from google.cloud import storage
from google.cloud.storage import Blob, Bucket, Client
from starlette import status

from src.settings import app_settings


def upload_file(file_name, to: str = None) -> Dict:
    return _upload_to_gcloud(source_file_name=file_name, destination_blob_name=to)


def _upload_to_gcloud(source_file_name, destination_blob_name) -> Dict:
    """
    Uploads a file to the bucket.
    :param source_file_name: The path to your file to upload (ex: "local/path/to/file")
    :param destination_blob_name: The ID of your GCS object (ex: "storage-object-name")
    :return:
    """
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    bucket_name = app_settings.BUCKET_NAME

    storage_client: Client = storage.Client()
    bucket: Bucket = storage_client.bucket(bucket_name)
    blob: Blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_filename(source_file_name)
    except Forbidden as e:
        logging.error(e)
        return {"status": status.HTTP_403_FORBIDDEN, "url": ""}

    logging.info("File {} uploaded to {}.".format(source_file_name, destination_blob_name))
    return {"status": status.HTTP_200_OK, "url": blob.public_url}
