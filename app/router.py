from fastapi import FastAPI, Depends
from app.auth import router as auth_router, get_current_user
from celery.result import AsyncResult
import app.worker as worker
from pydantic import BaseModel
import app.conversation_store as conversation_store

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
    task = worker.delay(req.message)
    
    return {
        "message": "AI request queued",
        "task_id": task.id,
        "user_id": user.user.id
    }
    
@app.post("/ask_bot")
async def ask_ai_to_execute_function(req: TalkWithAIRequest, user=Depends(get_current_user)):
    # Queue the task with Celery
    task = worker.ask_bot.delay(req.message)
    
    return {
        "message": "AI request queued",
        "task_id": task.id,
        "user_id": user.user.id
    }
    
@app.post("/ask_bot_custom_query")
async def ask_ai_to_create_custom_query(req: TalkWithAIRequest, user=Depends(get_current_user)):
    # Queue the task with Celery
    task = worker.ask_bot_custom_query.delay(
        message = req.message,
        user_id = user.user.id 
    )
    
    return {
        "message": "AI request queued",
        "task_id": task.id,
        "user_id": user.user.id
    }
    
@app.delete("/conversation/clear")
async def clear_conversation(user=Depends(get_current_user)):
    conversation_store.clear_conversation(user.user.id)
    return {"message": "Conversation history cleared"}

@app.get("/conversation/history")
async def get_conversation_history(user=Depends(get_current_user)):
    history = conversation_store.get_conversation_history(user.user.id)
    return {
        "user_id": user.user.id,
        "message_count": len(history),
        "history": history
    }

@app.get("/generate_insights")
async def generate_insights_endpoint(user=Depends(get_current_user)):
    task = worker.generate_insights.delay()
    
    return {
        "message": "Insights generation queued",
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