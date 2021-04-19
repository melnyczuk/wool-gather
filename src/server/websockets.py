import asyncio
from asyncio.events import AbstractEventLoop
from base64 import b64decode
from typing import List, Union

import cv2  # type:ignore
import numpy as np
import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.server import WebSocketServerProtocol

from src.app import ObjectDetector, TextGenerator
from src.app.utils import seed_from


class Server(object):
    host: str
    port: int
    object_detector: ObjectDetector
    text_generator: TextGenerator
    event_loop: AbstractEventLoop

    def run(self: "Server"):
        print(f"WS server: {self.host=} {self.port=}")
        start = websockets.serve(self.__handler, self.host, self.port)
        self.event_loop.run_until_complete(start)
        self.event_loop.run_forever()

    def __init__(self: "Server", host: str = "127.0.0.1", port: int = 4242):
        self.host = host
        self.port = port
        self.object_detector = ObjectDetector()
        self.text_generator = TextGenerator(model_dir="data/folktales")
        self.event_loop = asyncio.get_event_loop()

    async def __handler(
        self: "Server",
        websocket: WebSocketServerProtocol,
        path: str,
    ):
        try:
            data = await websocket.recv()
        except ConnectionClosedOK:
            return
        except ConnectionClosedError as err:
            print(f"WS connection closed unexpectedly: {err.code} {err.reason}")
            return

        coro = self.__route(path, data)
        task = self.event_loop.create_task(coro)
        result = await task

        try:
            await websocket.send(result)
        except ConnectionClosedOK:
            return
        except ConnectionClosedError as err:
            print(f"WS connection closed unexpectedly: {err.code} {err.reason}")
            return
        return

    async def __route(
        self: "Server",
        path: str,
        data: Union[str, bytes],
    ) -> str:
        if path == "/":
            return await self.__wool_gather(data)
        if path == "/ping":
            return await self.__ping()
        if path == "/text":
            return await self.__generate_text(str(data))
        if path == "/detect":
            classes = await self.__detect_objects(data)
            return ",".join(classes)
        return "Bad path"

    async def __ping(self: "Server") -> str:
        return "pong!"

    async def __wool_gather(self: "Server", frame: Union[bytes, str]) -> str:
        labels = await self.__detect_objects(frame)
        seed = seed_from(labels)
        text = await self.__generate_text(seed)
        return text

    async def __detect_objects(
        self: "Server", frame: Union[bytes, str]
    ) -> List[str]:
        arr = np.frombuffer(b64decode(frame), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
        return [label for (_, label, _) in self.object_detector.predict(img)]

    async def __generate_text(self: "Server", seed: str) -> str:
        return self.text_generator.generate(seed)


if __name__ == "__main__":
    server = Server()
    server.run()
