from DBEntities import UserEntity
import typing 
import random


async def user_exists(username :str) -> typing.AnyStr:
    
    return await UserEntity.filter(username = username).exists()
        
    
    
    
def generate_id_nums() -> str:
    """Generates a random 9-digit number and formats it as XXX-XXX-XXX."""
    number = random.randint(100_000_000, 999_999_999)  # Ensures a 9-digit number
    num_str = str(number)

    return f"{num_str[:3]}-{num_str[3:6]}-{num_str[6:]}"