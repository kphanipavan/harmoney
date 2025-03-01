from typing import Any, Dict
from websockets.asyncio import client as WSC
import asyncio
import pickle as pkl
from callSpec import CallPacket

__all__ = ["startRunner"]

async def test(funcMap: Dict[str, Any], url):
    counter=0
    async with WSC.connect(url, open_timeout=None, ping_interval=10, ping_timeout=None ) as w:
        id = await w.recv()
        id = int(id)
        print(f"Starting Runner, ID: {id}")
        await w.send({"methods":list(funcMap.keys())})
        while True:
            counter+=1
            packetBytes=await w.recv()
            callPk:CallPacket = pkl.loads(packetBytes)
            print("-"*50 + f"\nRunning: {callPk.procedure}\nArgs: {callPk.data}\n" + "-"*25)
            funcOutput = funcMap[callPk.procedure](**callPk.data)
            await w.send(str(counter))



def startRunner(funcMapping, host, port):
    asyncio.run(test(funcMapping, f"ws://{host}:{port}/reg"))
