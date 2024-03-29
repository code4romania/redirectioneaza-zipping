import logging
import random
import string
import time
from typing import Callable, List

from fastapi import BackgroundTasks, FastAPI, HTTPException
from requests import Request, Response
from starlette import status
from starlette.responses import JSONResponse

from src.models import Input
from src.settings import app_settings
from src.utils import send_notification
from storage.processor import clean_up_after_current_job, encode_file_names, zip_urls
from storage.uploader import upload_file

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get(
    "/teapot",
    summary="I'm a teapot",
    status_code=status.HTTP_418_IM_A_TEAPOT,
    description="Useful for testing the server and seeing if it works",
)
@app.post(
    "/teapot",
    summary="I'm a teapot",
    status_code=status.HTTP_418_IM_A_TEAPOT,
    description="Useful for testing the server and seeing if it works",
)
def teapot():
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail={"msg": "I'am a teapot."})


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
async def zip_documents(payload: Input, background_tasks: BackgroundTasks):
    if payload.passphrase is None or payload.passphrase != app_settings.SECRET_PASSPHRASE:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised request")

    if app_settings.RUNNING_MODE == "foreground":
        return _run_documents_uploader(payload)
    else:
        background_tasks.add_task(_run_documents_uploader, payload)

    return JSONResponse({"status": status.HTTP_200_OK, "message": "Task added to queue"})


def _run_documents_uploader(payload: Input):
    job_identifier: str = encode_file_names(payload.urls)

    try:
        _zip_documents(payload, job_identifier)
    finally:
        if app_settings.RUN_CLEAN_UP:
            clean_up_after_current_job(job_identifier)


def _zip_documents(payload: Input, job_identifier) -> JSONResponse:
    pdf_urls: List[str] = payload.urls

    zipped_file = zip_urls(pdf_urls, job_identifier)
    upload_response = upload_file(zipped_file, destination=payload.path)

    if status.HTTP_200_OK < upload_response["status"] >= status.HTTP_400_BAD_REQUEST:
        raise HTTPException(status_code=upload_response["status"], detail="Upload failed")

    notification_status: int = send_notification(payload.webhook, blob_url=upload_response["url"])

    if status.HTTP_200_OK < notification_status >= status.HTTP_400_BAD_REQUEST:
        raise HTTPException(status_code=notification_status, detail="Notification failed")

    return JSONResponse(content=upload_response)
