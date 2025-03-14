from tortoise.expressions import Q
from DBEntities.chatEntity import ChatEntity

async def get_or_create_chat(user_id: str, recipient_id: str):
    """
    Get an existing chat between two users or create a new one if it doesn't exist.
    """
    chat = await ChatEntity.filter(
        Q(participants__id=user_id) & Q(participants__id=recipient_id) & Q(is_group=False)
    ).first()

    if not chat:
        chat = await ChatEntity.create(is_group=False)
        await chat.participants.add(user_id, recipient_id)
        
    return chat

