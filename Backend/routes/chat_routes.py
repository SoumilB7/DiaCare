from fastapi import APIRouter
from models.chat import ChatLog
from db.database import chat_logs_collection

router = APIRouter()

# Store chat logs
@router.post("/store_chat")
async def store_chat(chat: ChatLog):
    await chat_logs_collection.insert_one(chat.dict())
    return {"message": "Chat stored successfully"}

# Retrieve chat logs
@router.get("/get_chat/{chatid}")
async def get_chat(chatid: str):
    chat = await chat_logs_collection.find_one({"chatid": chatid})
    if not chat:
        return {"message": "No chat found"}
    chat["_id"] = str(chat["_id"])  # Convert ObjectId to string
    return chat
