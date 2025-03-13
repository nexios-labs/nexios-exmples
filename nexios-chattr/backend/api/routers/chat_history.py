from nexios.routing import Router
from nexios.http import Request, Response
from DBEntities.chatEntity import ChatEntity
chat_history_router = Router(prefix="/chat")

@chat_history_router.get("/history")
async def get_chat_history(req: Request, res: Response):
    user = req.user
    if not user.is_authenticated:
        return res.json({"error": "User not authenticated"}, status_code=401)
    
    chat_history = await ChatEntity.filter(participants=user).all()
    
    return res.json({
        "chat_history": [chat.to_dict() for chat in chat_history]
    }, status_code=200)