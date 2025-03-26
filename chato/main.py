from nexios import get_application
from nexios.routing import WSRouter
from nexios.websockets.consumers import WebSocketEndpoint
from nexios.websockets import WebSocket
import time
import typing
import uuid
from .models import User,ChatMessage
from .utils import render_template

app = get_application()
ws_router = WSRouter()
active_users: typing.Dict[str, User] = {}
chat_rooms: typing.Dict[str, typing.List[str]] = {}  

@app.get("/")
async def home(req, res):
    return res.html(render_template("index.html"))
class ChatEndpoint(WebSocketEndpoint):
    def __init__(self, logging_enabled = True, logger = None):
        super().__init__(logging_enabled, logger)
        self.encoding = "json" #this will be fixed in 2.2.7
    async def on_connect(self, ws: WebSocket):
        await ws.accept()
        
       
        self.room_id = ws.query_params.get("room", "general")
        username = ws.query_params.get("username", f"Guest-{uuid.uuid4().hex[:6]}")
        
        
        user_id = str(uuid.uuid4())
        self.user = User(
            id=user_id,
            username=username,
            joined_at=time.time(),
            last_active=time.time()
        )
        active_users[user_id] = self.user
        
        # Initialize room if needed
        if self.room_id not in chat_rooms:
            chat_rooms[self.room_id] = []
        
        # Add user to room
        chat_rooms[self.room_id].append(user_id)
        
        # Join the WebSocket room
        await self.join_group(self.room_id)
        
        await self.broadcast_system_message(f"{username} joined the chat")
        
        # Send welcome message with room info
        await ws.send_json({
            "type": "welcome",
            "user": self.user.username,
            "userId": self.user.id,
            "room": self.room_id,
            "members": [active_users[uid].username for uid in chat_rooms[self.room_id]],
            "timestamp": time.time()
        })
    
    async def on_receive(self, ws: WebSocket, data: typing.Any):
        self.user.last_active = time.time()
        active_users[self.user.id] = self.user
        
        if data.get("type") == "message":
            content = data.get("content", "").strip()
            if not content:
                return
                
            message = ChatMessage(
                id=str(uuid.uuid4()),
                room_id=self.room_id,
                sender=self.user,
                content=content,
                timestamp=time.time()
            )
            
            await self.broadcast_message(message)
            
        elif data.get("type") == "typing":
            # Broadcast typing indicator
            await self.broadcast({
                "type": "typing",
                "user": self.user.username,
                "userId": self.user.id,
                "room": self.room_id,
                "timestamp": time.time()
            }, self.room_id)
    
    async def on_disconnect(self, ws: WebSocket, close_code: int):
        if hasattr(self, 'user') and hasattr(self, 'room_id'):
            # Remove user from room
            if self.room_id in chat_rooms and self.user.id in chat_rooms[self.room_id]:
                chat_rooms[self.room_id].remove(self.user.id)
                
                if not chat_rooms[self.room_id]:
                    chat_rooms.pop(self.room_id, None)
            
            active_users.pop(self.user.id, None)
            
            await self.broadcast_system_message(f"{self.user.username} left the chat")
            
            await self.leave_group(self.room_id)
    
    async def broadcast_message(self, message: ChatMessage):
        """Broadcast a chat message to the room"""
        await self.broadcast({
            "type": "message",
            "id": message.id,
            "room": message.room_id,
            "sender": message.sender.username,
            "senderId": message.sender.id,
            "content": message.content,
            "timestamp": message.timestamp
        }, self.room_id, save_history=True)
    
    async def broadcast_system_message(self, content: str):
        """Broadcast a system message to the room"""
        await self.broadcast({
            "type": "system",
            "content": content,
            "timestamp": time.time()
        }, self.room_id, save_history=True)



ws_router.add_ws_route(ChatEndpoint.as_route("/ws/chat"))
    
    
app.mount_ws_router(ws_router)
