from fastapi import APIRouter
from models.data import UserData
from db.database import data_collection

router = APIRouter()

# Save user data
@router.post("/save_data")
async def save_user_data(data: UserData):
    await data_collection.insert_one(data.dict())
    return {"message": "Data saved successfully"}

# Get user data
@router.get("/get_data/{userid}")
async def get_user_data(userid: str):
    data = await data_collection.find_one({"userid": userid})
    if not data:
        return {"message": "No data found"}
    data["_id"] = str(data["_id"])  # Convert ObjectId to string
    return data
