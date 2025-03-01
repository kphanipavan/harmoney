import requests as req
import callSpec
import numpy as np
import pickle as pkl
import base64
testNPArray = np.ones((3,3,3))
testObj = callSpec.CallPacket(procedure="sum",data={"a":testNPArray} )
x=req.post("http://127.0.0.1:7732/cliReq", json={"data":base64.b64encode(pkl.dumps(testObj)).decode("utf-8")})
testObj = callSpec.CallPacket(procedure="avg",data={"a":testNPArray} )
x=req.post("http://127.0.0.1:7732/cliReq", json={"data":base64.b64encode(pkl.dumps(testObj)).decode("utf-8")})
print(x.status_code)
print(x.text)
