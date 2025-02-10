from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from db.database import user_collection
from bson import ObjectId
import bcrypt

router = APIRouter()

# Hash password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

# Register User
@router.post("/register")
async def register_user(user: User):
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)
    new_user = {"username": user.username, "password": hashed_password}
    result = await user_collection.insert_one(new_user)
    return {"id": str(result.inserted_id), "username": user.username}

# Get all users
@router.get("/users")
async def get_users():
    users = await user_collection.find().to_list(100)
    return [{"id": str(user["_id"]), "username": user["username"]} for user in users]
