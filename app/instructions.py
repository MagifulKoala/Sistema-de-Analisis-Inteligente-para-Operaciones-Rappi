BUSINESS_DEFINITIONS = """
"""

GENERAL_PROMPT = """
You will be asked a specific question. Determine if there is a prebuilt function that you were passed on
that answers the question you were asked. If there is no available function, answer the question
in the best way you can making sure to prevent guessing or infering a response that would
need the results of the function. Respond with the following structure:
'Sorry, I don't appear to have access to that kind of functionalities yet. However...'.

Example:
For example, if the function 'get_email' exists and it returns the email of a user given his id, behave in the following way:

input: "given employee id 123 what is his email ?"
output: function call

input: "How many orders does the user 123 have ? "
output: "sorry, I don't appear to have access to a function like that. However, you can look it up in the database under the order column for that user"
"""

def get_instructions(user_instructions:str)->str:
    return f"""
    {GENERAL_PROMPT}
    
    To help you better understand the context of the questions being asked here are some business terminology and definitions:
    <<{BUSINESS_DEFINITIONS}>>
    
    Adress the following question:
    <<{user_instructions}>>
    """