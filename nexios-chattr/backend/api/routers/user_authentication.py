from nexios.routing import Router
from models.authentication_schema import UserLoginSchema
from nexios.http import Request, Response
from pydantic import ValidationError
import bcrypt
from DBEntities.userEntity import UserEntity
from nexios.config import get_config
from nexios.auth.backends.jwt import create_jwt
from ..services.user_manager import user_exists
import datetime
user_authentication_router = Router()

@user_authentication_router.post("/login")
async def login_user(req: Request, res: Response):
    request_data = await req.json
    try:
        validated_data = UserLoginSchema(**request_data)
    except ValidationError as e:
        error = e.errors()
        print(error)
        return res.status(422)
    
    data = dict(validated_data)
    
    if not await user_exists(data['username']):
        return res.json({
            "error": "Invalid username or password!"
        }, status_code=400)
    
    user = await UserEntity.get(username=data['username'])
    
    if not bcrypt.checkpw(data['password'].encode("utf-8"), user.hashed_password.encode("utf-8")):
        return res.json({
            "error": "Invalid username or password!"
        }, status_code=400)
    
    
    config = get_config().secret_key
    
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = create_jwt({
        "username":user.username,
        "phone":user.phone,
        "id":user.id,
         "exp":expiration_time
    })
    return res.json({
        "message": "Login successful!",
        "user": {
            "username": user.username,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio
        },
        "token":token
    }, status_code=200)