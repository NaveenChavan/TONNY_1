from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Conversation:
    id: int
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str
    session_id: Optional[str] = None

@dataclass
class Preference:
    key: str
    value: str
    created: str
    updated: str