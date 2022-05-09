from typing import Dict

from requests import Response, post

from src.models import WebhookInput


def send_notification(webhook_data: WebhookInput, blob_url: str) -> int:
    webhook_url: str = webhook_data.url
    webhook_payload: Dict = webhook_data.data
    webhook_payload["url"] = blob_url

    response: Response = post(webhook_url, json=webhook_payload)

    return response.status_code
