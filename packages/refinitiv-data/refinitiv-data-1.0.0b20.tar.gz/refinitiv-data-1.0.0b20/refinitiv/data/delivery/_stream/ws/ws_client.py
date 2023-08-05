import json
from typing import Callable, List, Dict

import websocket


class WebSocketClient:
    def __init__(
        self, on_message: Callable[[List[Dict]], None], *args, **kwargs
    ) -> None:
        self._on_message = on_message
        self.ws = websocket.WebSocketApp(
            on_message=self._on_ws_message, *args, **kwargs
        )

    def _on_ws_message(self, ws: websocket.WebSocketApp, s: str) -> None:
        try:
            messages = json.loads(s)
        except UnicodeDecodeError:
            messages = "".join(map(chr, bytearray(s)))
            messages = json.loads(messages)
        self._on_message(messages)

    def send(self, data: dict) -> None:
        self.ws.send(json.dumps(data))

    def run_forever(self, *args, **kwargs) -> None:
        self.ws.run_forever(*args, **kwargs)

    def close(self, **kwargs) -> None:
        self.ws.close(**kwargs)
