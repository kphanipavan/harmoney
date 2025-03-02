import requests as req
from ._callSpec import _CallPacket
import pickle as pkl
import base64

__all__ = ["Client"]

class Client:
    def __init__(self, host, port) -> None:
        self._url = f"http://{host}:{port}/cliReq"

    def rCall(self, function, **kwargs):
        callPacket = _CallPacket(procedure=function, data=kwargs)
        payload = {"data": base64.b64encode(pkl.dumps(callPacket)).decode("utf-8")}
        resp = req.post(self._url, json=payload)
        # print(resp.status_code)
        # print(resp.text)
        return pkl.loads(base64.b64decode(resp.text))
