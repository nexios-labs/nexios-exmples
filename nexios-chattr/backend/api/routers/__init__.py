from .user_creation import user_creation_router
from .user_authentication import user_authentication_router
from .chat_history import chat_history_router
from nexios.routing import Router



api_router = Router(prefix="/api") #main api router



#auth router
auth_router = Router(prefix="/auth") #main api router


auth_router.mount_router(user_creation_router)
auth_router.mount_router(user_authentication_router)



#chat history 

api_router.mount_router(chat_history_router)



api_router.mount_router(auth_router)
