from fastapi import FastAPI, Depends
from app.auth import router as auth_router, get_current_user
from app.worker import talk_with_ai
from pydantic import BaseModel

app = FastAPI()
app.include_router(auth_router)

class TalkWithAIRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"Hello":"World"}


@app.post("/talk_with_ai")
async def talk_with_ai_endpoint(req: TalkWithAIRequest, user=Depends(get_current_user)):
    # Queue the task with Celery
    task = talk_with_ai.delay(req.message)
    
    return {
        "message": "AI request queued",
        "task_id": task.id,
        "user_id": user.user.id
    }