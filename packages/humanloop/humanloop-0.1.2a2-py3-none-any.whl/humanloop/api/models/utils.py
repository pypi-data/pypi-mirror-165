from pydantic import BaseModel
from typing import Dict, Any


KeyValues = Dict[str, Any]


class RootBaseModel(BaseModel):
    def dict(self, **kwargs):
        output = super().dict(**kwargs)
        return output["__root__"]
