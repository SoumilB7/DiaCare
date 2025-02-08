from pydantic import BaseModel
from typing import List, Dict

class ChatEntry(BaseModel):
    system: str
    user: str
    assistant: str

class ChatLog(BaseModel):
    chatid: str
    chat: List[Dict[str, str]]  # Store chat as a list of {role: message}
