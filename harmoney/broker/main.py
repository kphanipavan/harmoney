import asyncio
import base64
from uvicorn import Config, Server
import fastapi
from uvicorn.config import LOG_LEVELS
import pickle as pkl
from callSpec import CallPacket, ClientPacket

__all__ = ["runBroker"]

class Broker:
    def __init__(self) -> None:
        self.router = fastapi.APIRouter()
        self.router.add_api_websocket_route("/reg", self.registerRunner)
        self.router.add_api_route("/cliReq", self.clientRequest, methods=["POST"])
        self.taskQueue = asyncio.Queue()
        self.runnerCount=0


    async def registerRunner(self,  wsConnection: fastapi.WebSocket):
        await wsConnection.accept()
        await wsConnection.send_text(str(self.runnerCount))
        methods=await wsConnection.receive_json()
        print(f"Runner Connected with ID: {self.runnerCount}, Methods: {methods['methods']}")
        self.runnerCount+=1
        while True:
            data:CallPacket = await self.taskQueue.get()
            # await asyncio.sleep(1)
            await wsConnection.send_bytes(pkl.dumps(data))
            retValue = await wsConnection.receive()
            print(f"Tasks left: {self.taskQueue.qsize()}")

    async def clientRequest(self, data:ClientPacket):
        print(data)
        callPacket = pkl.loads(base64.b64decode(data.data))
        await self.taskQueue.put(callPacket)
        print(self.taskQueue.qsize)
        # await self.taskQueue.put(name)

def runBroker(host, port):
    br = Broker()
    app = fastapi.FastAPI()
    app.include_router(br.router)
    serverConf = Config(app = app, host=host,  port=port, log_level=LOG_LEVELS["warning"], ws_ping_interval=10, ws_ping_timeout=None)
    server = Server(config=serverConf)
    server.run()

# runBroker()
