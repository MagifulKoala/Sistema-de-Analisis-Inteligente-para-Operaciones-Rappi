from celery import Celery
import app.gemini as gemini
import app.conversation_store as conv_store

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

@app.task
def ask_bot_custom_query(message: str, user_id: str):
    history = conv_store.get_conversation_history(user_id)
    
    formatted_history = []
    for entry in reversed(history):
        formatted_history.append({
            'user': entry['message'],
            'assistant': entry['response']
        })
        
    result = gemini.ask_ai_to_create_custom_function(
        contents=message,
        conversation_history=formatted_history
    )
    
    conv_store.add_to_conversation(
        user_id=user_id,
        message=message,
        response=str(result['response'])
    )
    
    return result['response']