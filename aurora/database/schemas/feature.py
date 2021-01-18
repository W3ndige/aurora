from typing import List
from pydantic import BaseModel


class Feature(BaseModel):
    data: List
    type: str
