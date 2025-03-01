import requests as req
import callSpec
import pickle as pkl
import base64
# testNPArray = np.random.random((3,3,3, 3))
# testObj = callSpec.CallPacket(procedure="sum",data={"a":testNPArray} )
# x=req.post("http://127.0.0.1:7732/cliReq", json={"data":base64.b64encode(pkl.dumps(testObj)).decode("utf-8")})
# testObj = callSpec.CallPacket(procedure="avg",data={"a":testNPArray} )
# x=req.post("http://127.0.0.1:7732/cliReq", json={"data":base64.b64encode(pkl.dumps(testObj)).decode("utf-8")})
# print(x.status_code)
# print(x.text)

class Client:
    def __init__(self, host, port) -> None:
        self.url = f"http://{host}:{port}/cliReq"

    def rCall(self, function, **kwargs):
        callPacket = callSpec.CallPacket(procedure=function, data=kwargs)
        payload = {"data": base64.b64encode(pkl.dumps(callPacket)).decode("utf-8")}
        resp = req.post(self.url, json=payload)
        print(resp.status_code)
        print(resp.text)
        return resp
