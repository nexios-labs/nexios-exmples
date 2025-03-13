from nexios.routing import Router
from models.authentication_schema import UserCreationSchema
from nexios.http import Request,Response
from pydantic import ValidationError
import bcrypt
from DBEntities.userEntity import UserEntity
from ..services.user_manager import user_exists,generate_id_nums
user_creation_router = Router("/users")




@user_creation_router.post("/new")
async def create_user(req :Request, res :Response):
    request_data = await req.json
    try:
        validated_data = UserCreationSchema(**request_data)
    except ValidationError as e:
        error = e.errors()
        print(error)
        return res.status(422)
    
    data = dict(validated_data)
    
    if await user_exists(data['username']):
        return res.json({
            "error":"username already taken !"
        },status_code=400)
        
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(data['password'].encode("utf-8"), salt).decode("utf-8")
    await UserEntity.create(**data,hashed_password = hashed_password,phone = generate_id_nums())
    return res.json(request_data)


@user_creation_router.post("/check-username/{username:str}")
async def check_username(req: Request, res: Response):
    """Checks if a username is already taken."""
    username = req.path_params.username
    if await user_exists(username):
        return res.json({"exists": True}, status_code=200)
    
    return res.json({"exists": False}, status_code=200)