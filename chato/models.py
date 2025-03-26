from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import uuid

@dataclass
class User:
    id: str
    username: str
    joined_at: datetime
    last_active: datetime

@dataclass
class ChatMessage:
    id: str
    room_id: str
    sender: User
    content: str
    timestamp: datetime
    message_type: str = "chat"  # Can be 'chat', 'system', etc.