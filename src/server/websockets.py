import asyncio
import json
from dataclasses import dataclass
from asyncio.events import AbstractEventLoop
from base64 import b64decode
from typing import Dict, List, Union

import cv2  # type:ignore
import numpy as np
import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.server import WebSocketServerProtocol

from src.app import ObjectDetector, TextGenerator
from src.app.utils import seed_from


@dataclass
class Settings:
    test: str = "hello"
    line_len: int = 50


class Server(object):
    host: str
    port: int
    settings: Settings
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
        self.settings = Settings()
        self.object_detector = ObjectDetector()
        self.text_generator = TextGenerator()
        self.event_loop = asyncio.get_event_loop()

    def __set_settings(self: "Server", data):
        self.settings = Settings(**data)
        print(f"Settings: {self.settings}")
        return

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
            await websocket.send(json.dumps(result))
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
    ) -> Union[str, Dict[str, List[str]]]:
        if path == "/":
            labels = await self.__detect_objects(data)
            seed = seed_from(labels)
            text = await self.__generate_text(seed)
            return {"text": text, "labels": labels}

        if path == "/settings":
            self.__set_settings(json.loads(data))
            return "OK"

        if path == "/text":
            text = await self.__generate_text(str(data))
            return {"text": text}

        if path == "/detect":
            classes = await self.__detect_objects(data)
            return {"labels": classes}

        return "Bad path"

    async def __detect_objects(
        self: "Server", frame: Union[bytes, str]
    ) -> List[str]:
        arr = np.frombuffer(b64decode(frame), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
        return [label for (_, label, _) in self.object_detector.predict(img)]

    async def __generate_text(self: "Server", seed: str) -> List[str]:
        return self.text_generator.sentences(
            seed,
            line_len=self.settings.line_len,
        )


if __name__ == "__main__":
    server = Server()
    server.run()
