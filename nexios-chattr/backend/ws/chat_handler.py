from nexios.websockets.consumers import WebSocketEndpoint
from nexios import routing


chat_router = routing.WSRouter(prefix="/chat")
class ChatHandler(WebSocketEndpoint):
    
    async def on_connect(self, websocket):
        await super().on_connect(websocket)
        self.join_group("user_chats")
        
        
        

chat_router.add_ws_route(
    route=routing.WebsocketRoutes(
        path="/{user_id}",
        handler=ChatHandler(
            logging_enabled=True
            
            )
    )
)