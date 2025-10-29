from celery import Celery
from gemini import ask_ai_something

app = Celery("tasks", broker="redis://redis:6379/0")

@app.task
def talk_with_ai(message: str):
    ask_ai_something(message)