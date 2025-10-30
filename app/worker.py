from celery import Celery
import app.gemini as gemini

app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

app.conf.result_expires = 3600

@app.task
def talk_with_ai(message: str):
    return gemini.ask_ai_something(message)

@app.task
def ask_bot(message: str):
    return gemini.ask_ai_to_execute_function(message)