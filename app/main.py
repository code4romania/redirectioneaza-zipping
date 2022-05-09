import logging
import random
import string
import time
from typing import Callable, List

from fastapi import BackgroundTasks, FastAPI, HTTPException
from requests import Request, Response
from starlette import status
from starlette.responses import JSONResponse

from src.file_management import urls_to_zip
from src.models import Input
from src.settings import app_settings
from src.uploader import upload_file
from src.utils import send_notification

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
async def zip_documents(payload: Input, background_tasks: BackgroundTasks):
    if settings.RUNNING_MODE == "foreground":
        return _zip_documents(payload)
    else:
        background_tasks.add_task(_zip_documents, payload)

    return {"message": "All went well"}


def _zip_documents(payload: Input) -> JSONResponse:
    pdf_urls: List[str] = payload.urls
    zipped_file = urls_to_zip(pdf_urls)
    upload_response = upload_file(zipped_file, destination=payload.path)

    if status.HTTP_200_OK < upload_response["status"] >= status.HTTP_400_BAD_REQUEST:
        raise HTTPException(status_code=upload_response["status"], detail="Upload failed")

    notification_status: int = send_notification(payload.webhook, blob_url=upload_response["url"])

    if status.HTTP_200_OK < notification_status >= status.HTTP_400_BAD_REQUEST:
        raise HTTPException(status_code=notification_status, detail="Notification failed")

    # json_compatible_item_data = jsonable_encoder({"status": status, "url": upload_response["url"]})
    return JSONResponse(content=upload_response)
