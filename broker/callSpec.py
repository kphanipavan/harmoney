from typing import Any, Dict

import pydantic

class CallPacket(pydantic.BaseModel):
    procedure: str
    simpleObjects: Dict[str, Any] = {}
    byteObjects: Dict[str, bytes] = {}
