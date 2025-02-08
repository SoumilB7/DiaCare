# routes/__init__.py

# Import routers to make them available at the package level
from .user_routes import router as user_router
from .data_routes import router as data_router
from .chat_routes import router as chat_router

__all__ = ["user_router", "data_router", "chat_router"]
