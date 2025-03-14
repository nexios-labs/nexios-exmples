from nexios.websockets.consumers import WebSocketEndpoint
from nexios.websockets.base import WebSocket
from nexios import routing
import typing
from .services.auth_ws import authenticate_user,WebSocketException

chat_router = routing.WSRouter(prefix="/chat")
class ChatHandler(WebSocketEndpoint):
    encoding = "json"
    

    async def on_connect(self, websocket: WebSocket) -> None:
        await self.join_group("default")
        await super().on_connect(websocket)

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await self.broadcast(data, group_name="defaults", save_history=True)
 
        
        
        

chat_router.add_ws_route(
    route=routing.WebsocketRoutes(
        
        path="/{user_id}",
        handler=ChatHandler(
            logging_enabled=True
            
            )
    )
)