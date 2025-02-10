# db/__init__.py

# Import database collections to make them available
from .database import (
    user_collection,
    data_collection,
    chat_collection,
    chat_logs_collection
)

__all__ = [
    "user_collection",
    "data_collection",
    "chat_collection",
    "chat_logs_collection"
]
