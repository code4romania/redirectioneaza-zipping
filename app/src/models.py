from typing import Dict, List

from pydantic import BaseModel


class WebhookInput(BaseModel):
    url: str
    data: Dict


class Input(BaseModel):
    urls: List[str]
    path: str | None
    webhook: WebhookInput
    passphrase: str
