from typing import Dict, List

from pydantic import BaseModel


class Input(BaseModel):
    urls: List[str]
    path: str
    webhook: Dict
