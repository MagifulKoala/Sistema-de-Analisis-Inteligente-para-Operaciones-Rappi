from fastapi import FastAPI, Depends
from app.auth import router as auth_router, get_current_user
from celery.result import AsyncResult
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
    print(f" the type for the message is: {type(req.message)}")
    task = talk_with_ai.delay(req.message)
    
    return {
        "message": "AI request queued",
        "task_id": task.id,
        "user_id": user.user.id
    }
    
    
@app.get("/task/{task_id}")
async def get_task_status(task_id: str, user=Depends(get_current_user)):
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'PENDING':
        return {
            "task_id": task_id,
            "status": "pending",
            "result": None
        }
    elif task_result.state == 'SUCCESS':
        return {
            "task_id": task_id,
            "status": "success",
            "result": task_result.result
        }
    elif task_result.state == 'FAILURE':
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(task_result.info)
        }
    else:
        return {
            "task_id": task_id,
            "status": task_result.state,
            "result": task_result.info
        }