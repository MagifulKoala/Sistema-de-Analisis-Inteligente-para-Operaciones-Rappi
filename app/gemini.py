from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

import app.function_definitions as fd
import app.functions as f 
import app.instructions as instructions
import datasets.perform_query as perform_query

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=GEMINI_KEY)

tools = types.Tool(function_declarations=[ function_content for _, function_content in fd.function_schema_registry.items()])
config = types.GenerateContentConfig(tools=[tools])


def ask_ai_something(contents:str):
    model="gemini-2.5-flash-lite"
    resp = client.models.generate_content(
        model = model,
        contents=contents
    )
    return resp.text
    
    
def ask_ai_to_create_custom_function(contents:str, conversation_history:list = None):
    print("executing ask_ai_to_create_custom_function")
    
    model="gemini-2.5-flash-lite"
    if conversation_history is None:
        conversation_history = []
    
    resp = client.models.generate_content(
        model = model,
        contents=instructions.get_instructions_custom_AI_queries(
            user_instructions=contents,
            chat_history = str(conversation_history)
            )
    )
    print(f" current AI response: \n {resp.text} \n")
    
    if resp.text.split("|")[0].strip() == "-1":
        result = resp.text
    else:
        answer = str(perform_query.run_query(resp.text))
        result =  ai_analyze_results(
            user_query=contents,
            results=answer
        )
    
    return {
        "response": result,
        "conversation_history": conversation_history + [resp.text]
    }

def ai_analyze_results(user_query:str, results:str)-> str:
    model="gemini-2.5-flash-lite"
    resp = client.models.generate_content(
        model = model,
        contents=instructions.get_instructions_data_interpretation(user_query=user_query, query_results=results)
    )
    print(f"Response for ai_analyze_results is : {resp.text}")
    return {
        "user_query" : user_query,
        "query_results" : results,
        "analysis" : resp.text
    }

def ask_ai_to_execute_function(contents: str):
    
    model="gemini-2.5-flash-lite"
    
    resp = client.models.generate_content(
        model = model,
        contents=instructions.get_instructions(contents),
        config=config
    )
    
        # Check for a function call
    if resp.candidates[0].content.parts[0].function_call:
        function_call = resp.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        arguments = function_call.args
        print(f"Function to call: {function_name}")
        print(f"Arguments: {arguments}")
        
        return f.execute_function(function_name,arguments)
    else:
        print("No function call found in the response.")
        return resp.text