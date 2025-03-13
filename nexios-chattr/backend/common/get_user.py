from DBEntities import UserEntity
import typing
async def get_user(**kwargs :typing.Dict[str, typing.Any]) -> UserEntity:
    
    user_id = kwargs.get("id")
    user = await UserEntity.get_or_none(id = user_id)
    return user