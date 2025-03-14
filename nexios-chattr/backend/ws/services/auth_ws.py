from nexios.exceptions import WebSocketException
from DBEntities import UserEntity
from nexios.auth.backends.jwt import decode_jwt
from nexios.config import get_config
class WsAuthentication(WebSocketException):
    """Custom exception for WebSocket authentication errors."""
    pass


async def authenticate_user(payload):
    """
    Authenticate a user based on the WebSocket payload.

    Args:
        payload (dict): The incoming WebSocket message payload.

    Returns:
        dict: The authenticated user data if successful.

    Raises:
        WsAuthentication: If authentication fails.
    """
    is_auth = payload.get("type") == "auth"
    
    if not is_auth:
        raise WsAuthentication("Invalid authentication type")

    token = payload.get("token")
    
    if not token:
        raise WsAuthentication("Missing authentication token")

    # Simulate user authentication (Replace with actual logic)
    user = await get_user_from_token(token)
    
    if not user:
        raise WsAuthentication("Invalid or expired token")

    return user


async def get_user_from_token(token):
    """
    Simulated function to get a user from a token.
    
    Replace this with actual token verification logic.

    Args:
        token (str): The authentication token.

    Returns:
        dict or None: User data if the token is valid, else None.
    """
    secret_key :str = get_config().secret_key
    try:
        jwt_data = decode_jwt(token = token, secret=secret_key)
    except Exception as _:
        return 
    
    user = await UserEntity.get_or_none(
        id = jwt_data['id']
    )
    if not user:
        return 
    
    return user

