from celery import Celery
from app.gemini import ask_ai_something

app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

app.conf.result_expires = 3600

@app.task
def talk_with_ai(message: str):
    return ask_ai_something(message)