import requests as req
from websockets.asyncio import client as WSC
import asyncio

async def test(func):
    counter=0
    async with WSC.connect("ws://0.0.0.0:7732/reg", open_timeout=None, ping_interval=10, ping_timeout=None ) as w:
        while True:
            counter+=1
            x=await w.recv()
            await asyncio.sleep(1)
            func()
            print(x)
            await w.send(str(counter), text=True)



asyncio.run(test(print))
