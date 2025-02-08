from fastapi import FastAPI
from routes import user_router, data_router, chat_router

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI + MongoDB Backend",
    description="A backend API using FastAPI and MongoDB with Motor.",
    version="1.0.0"
)

# Include routers from different modules
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(data_router, prefix="/data", tags=["Data"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI + MongoDB Backend"}

