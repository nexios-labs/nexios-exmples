from tortoise import fields 
from tortoise.models import Model


class ChatEntity(Model):
    id = fields.UUIDField(pk=True)
    is_group = fields.BooleanField(default=False)
    participants = fields.ManyToManyField("models.UserEntity", related_name="chats")

class MessageEntity(Model):
    id = fields.UUIDField(pk=True)
    sender = fields.ForeignKeyField("models.UserEntity", related_name="sent_messages", on_delete=fields.CASCADE)
    receiver = fields.ForeignKeyField("models.UserEntity", related_name="received_messages", on_delete=fields.CASCADE)
    chat = fields.ForeignKeyField("models.ChatEntity", related_name="messages", on_delete=fields.CASCADE)
    
    message_type = fields.CharField(max_length=50, choices=["text", "image", "video", "file", "audio"])
    content = fields.TextField(null=True)  # Nullable for non-text messages
    media_url = fields.TextField(null=True)  # URL for media files

    status = fields.CharField(max_length=20, choices=["sent", "delivered", "read"], default="sent")
    is_deleted = fields.BooleanField(default=False)

    reply_to = fields.ForeignKeyField("models.MessageEntity", related_name="replies", null=True, on_delete=fields.SET_NULL)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "messages"
        ordering = ["-created_at"]  # Show recent messages first
