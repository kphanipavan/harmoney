from websockets.asyncio import client as WSC
import asyncio
import pickle as pkl
import numpy as np

from callSpec import CallPacket

async def test(funcMap):
    counter=0
    async with WSC.connect("ws://0.0.0.0:7732/reg", open_timeout=None, ping_interval=10, ping_timeout=None ) as w:
        while True:
            counter+=1
            packetBytes=await w.recv()
            callPk:CallPacket = pkl.loads(packetBytes)
            # await asyncio.sleep(1)
            print(callPk)
            print(funcMap[callPk.procedure](**callPk.data))
            await w.send(str(counter), text=True)


funcMapping = {"sum": np.sum, "avg": np.average}

asyncio.run(test(funcMapping))
