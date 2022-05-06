import logging
import random
import string
import time
from typing import Callable, Dict, List

from fastapi import FastAPI, HTTPException, BackgroundTasks
from requests import Request, Response
from starlette import status

from src.file_management import urls_to_zip
from src.uploader import upload_file
from src.utils import send_notification
from src.settings import app_settings

app = FastAPI()
settings = app_settings
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Response:
    idem: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time: float = time.time()

    response: Response = await call_next(request)

    process_time: float = (time.time() - start_time) * 1000
    formatted_process_time: str = "{0:.2f}".format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.post("/zip-docs", status_code=status.HTTP_200_OK)
async def zip_documents(payload: Dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(_zip_documents, payload)

    return {"message": "All went well"}


def _zip_documents(payload: Dict) -> None:
    pdf_urls: List[str] = payload["urls"]
    zipped_file = urls_to_zip(pdf_urls)
    upload_status = upload_file(zipped_file, to=payload["path"])

    if status.HTTP_200_OK < upload_status >= status.HTTP_400_BAD_REQUEST:
        raise HTTPException(status_code=upload_status, detail="Upload failed")

    notification_status: int = send_notification(payload["webhook"])

    if status.HTTP_200_OK < notification_status >= status.HTTP_400_BAD_REQUEST:
        raise HTTPException(status_code=notification_status, detail="Notification failed")
