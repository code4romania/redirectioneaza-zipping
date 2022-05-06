from typing import Dict

from requests import Response, post


def send_notification(webhook_data: Dict) -> int:
    webhook_url: str = webhook_data["url"]
    webhook_payload: Dict = webhook_data["data"]

    response: Response = post(webhook_url, json=webhook_payload)

    return response.status_code
