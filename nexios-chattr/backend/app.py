from nexios import get_application,NexiosApp
from nexios.auth.middleware import AuthenticationMiddleware
from nexios.auth.backends import JWTAuthBackend
from config import test_config,db_config
from api.routers import api_router
from tortoise import Tortoise as db
from common.get_user import get_user
from ws import WebsocketRouter
app = get_application(
    config=test_config
)




@app.on_startup
async def init_db():
    
    await db.init(
        config=db_config
    )
    print("Database Connected")



@app.on_shutdown
async def close_db():
    await db.close_connections()
    print("Database closed")
app.mount_router(api_router)
app.mount_ws_router(WebsocketRouter)
app.add_middleware(
    middleware=AuthenticationMiddleware(
        backend=JWTAuthBackend(
            authenticate_func=get_user
        )
    )
)