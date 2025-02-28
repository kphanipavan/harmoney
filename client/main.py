import requests as req
import callSpec


testObj = callSpec.CallPacket(procedure="arstarst", simpleObjects={"arst":"qwfpp"})
print(testObj.model_dump_json())
x=req.post("http://127.0.0.1:7732/cliReq", json=testObj.model_dump())
print(x.status_code)
print(x.text)
