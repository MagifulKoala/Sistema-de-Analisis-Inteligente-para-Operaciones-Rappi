from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

import app.function_definitions as fd
import app.functions as f 
import app.instructions as instructions

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