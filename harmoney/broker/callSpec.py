from typing import Any, Dict

import pydantic

class CallPacket(pydantic.BaseModel):
    procedure: str
    data: Dict[str, Any] = {}

class ClientPacket(pydantic.BaseModel):
    data: str
