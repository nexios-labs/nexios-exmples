from nexios import routing
from .chat_handler import chat_router

WebsocketRouter = routing.WSRouter(prefix="/ws")

WebsocketRouter.mount_router(chat_router)