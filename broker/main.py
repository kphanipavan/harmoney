import asyncio
from typing import Dict
from uvicorn import Config, Server
import fastapi
from threading import Thread

from uvicorn.config import LOG_LEVELS

from callSpec import CallPacket


class Broker:
    def __init__(self) -> None:
        self.runnerQueue = []
        self.router = fastapi.APIRouter()
        self.router.add_api_websocket_route("/reg", self.registerRunner)
        self.router.add_api_route("/cliReq", self.clientRequest, methods=["POST"])
        self.taskQueue = asyncio.Queue()


    async def registerRunner(self,  wsConnection: fastapi.WebSocket):

        await wsConnection.accept()

        print("started")
        while True:
            data = await self.taskQueue.get()
            # await asyncio.sleep(1)
            await wsConnection.send_text(data)
            print(await wsConnection.receive())
            print(f"left: {self.taskQueue.qsize()}")

    async def clientRequest(self, data:CallPacket):
        print(data)
        # await self.taskQueue.put(name)

def runBroker():
    br = Broker()
    app = fastapi.FastAPI()
    app.include_router(br.router)
    serverConf = Config(app = app, host="0.0.0.0", port=7732, log_level=LOG_LEVELS["trace"], ws_ping_interval=10, ws_ping_timeout=None)
    server = Server(config=serverConf)
    server.run()

runBroker()
