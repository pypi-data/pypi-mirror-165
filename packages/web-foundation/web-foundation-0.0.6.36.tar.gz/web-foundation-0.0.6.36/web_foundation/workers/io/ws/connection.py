from typing import Any

from sanic.server.websockets.impl import WebsocketImplProtocol

from sanic import Websocket

from web_foundation.workers.io.rt_connection import WriteableObj, RtConnection


class WriteableWs(WriteableObj):
    obj: WebsocketImplProtocol

    def __init__(self, obj: WebsocketImplProtocol):
        super().__init__(obj)

    async def write(self, message: Any) -> None:
        await self.obj.send(message)


class WsRtConnection(RtConnection):
    pass
