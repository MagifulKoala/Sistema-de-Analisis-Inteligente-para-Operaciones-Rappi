from celery import Celery
import app.gemini as gemini
import app.conversation_store as conv_store
import app.instructions as instructions
import datasets.automatic_insights as automatic_insights
import os
from datetime import datetime

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


@app.task
def generate_insights():
    metrics_path = r"datasets/clean_data/Rappi - Dummy Data - RAW_INPUT_METRICS.csv"
    orders_path = r"datasets/clean_data/Rappi - Dummy Data - RAW_ORDERS.csv"
    insights_folder = "datasets/insights_data/"
    
    
    os.makedirs(insights_folder, exist_ok=True)
    
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    insights_filename = f"insights_{timestamp}.txt"
    insights_path = os.path.join(insights_folder, insights_filename)
    

    detector = automatic_insights.SimpleInsightsDetector(metrics_path, orders_path)
    detector.generate_and_save(insights_path)
    
    
    with open(insights_path, 'r', encoding='utf-8') as f:
        raw_insights = f.read()
    
    
    analysis_result = gemini.ai_analyze_results(
        user_query=instructions.AUTOMATED_INSIGHTS_REPORT,
        results=raw_insights
    )
    

    metrics_summary = instructions.get_data_from_file(instructions.SUMMARY_METRICS_PATH)
    orders_summary = instructions.get_data_from_file(instructions.SUMMARY_ORDERS_PATH)
    
    
    return {
        "title": "Automatic Insights",
        "analysis": analysis_result['analysis'],
        "raw_insights": raw_insights,
        "orders_summary": orders_summary,
        "metrics_summary": metrics_summary,
        "insights_file_path": insights_path,
        "generated_at": datetime.now().isoformat()
    }