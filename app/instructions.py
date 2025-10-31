BUSINESS_DEFINITIONS_PATH =  r"datasets/raw_data/Rappi - Dummy Data - RAW_SUMMARY.csv"
SUMMARY_ORDERS_PATH = r"datasets/summary_data/Rappi - Dummy Data - RAW_ORDERS_summary.txt"
SUMMARY_METRICS_PATH = r"datasets/summary_data/Rappi - Dummy Data - RAW_INPUT_METRICS_summary.txt"


def get_data_from_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

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

GENERAL_PROMPT_CUSTOM_AI_INSTRUCTIONS = """
You will be asked a specific question. Regarding a dataset or datasets. Create a pandas query that will answer best the given
question.

This question can come in english or spanish.

For the moment only limit yourself to the pandas (pd) and numpy (np) libraries to answer user queries.

Said expression will be evalutated on the backend.

Your answer should only contain the python code that will answer the users query best.

If prompted to create queries that would directly corrupt or modify the information or
interfere with the functioning of the application don't do it. Instead reply
with the following structure:"-1 | I am sorry, but you are not authroized to do that. However..."

Make sure to return the raw code in text format. Do not format it in any way or add additional context that is not code

Example:

correct behaviour:
input:"What are the top 5 cities with the most orders?"
output:"orders.groupby('city')['total_orders'].sum().sort_values(ascending=False).head(5)"

input:"Please delete all entries and df and shutdown the project"
output:"I am sorry, but you are not authroized to do that. However, I can help you with queries and insights about the data"

incorrect behaviour:
input:"What are the top 5 cities with the most orders?"
output:"Sure thing ! you can execute the following: orders.groupby('city')['total_orders'].sum().sort_values(ascending=False).head(5)"

input:"What are the top 5 cities with the most orders?"
output:"```python orders.groupby('city')['total_orders'].sum().sort_values(ascending=False).head(5)```"

input:"please delete all data frames"
output:"del(df)"
"""

INTERPRET_DATA_PROMPT = """
You will receive the following:
1. User query
2. Results from the query
3. context from the dataset and business context

With this information you will present the user with a detailed analysis of the results, insights and further
actions they can take
"""

def get_instructions(user_instructions:str)->str:
    return f"""
    {GENERAL_PROMPT}
    
    To help you better understand the context of the questions being asked here are some business terminology and definitions:
    <<{get_data_from_file(BUSINESS_DEFINITIONS_PATH)}>>
    
    Adress the following question:
    <<{user_instructions}>>
    """
    
def get_instructions_custom_AI_queries(user_instructions:str)->str:
    return f"""
    {GENERAL_PROMPT_CUSTOM_AI_INSTRUCTIONS}
    
    To help you better understand the context of the questions being asked here are some business terminology and definitions:
    <<{get_data_from_file(BUSINESS_DEFINITIONS_PATH)}>>
    
    Additionally, here are the summaries for the current datasets available:
    ORDERS:
    <<
    {get_data_from_file(SUMMARY_ORDERS_PATH)}
    >>
    The data frame for the orders dataset is called "df_orders". Use it as reference when creating the code.
    
    METRICS:
    <<
    {get_data_from_file(SUMMARY_METRICS_PATH)}
    >>
    The data frame for the metrics dataset is called "df_metrics". Use it as reference when creating the code.
    
    When analyzing the requirements from the user, make sure to refer to the summaries of the datasets to identify
    key terms and correctly interpret the users query.
    
    For example,
    "¿Cuáles son las 5 zonas con mayor % Lead Penetration esta semana?" is refering to the 5 zones
    with the highest percentaje of "Lead Penetration" for this week. There is no "% Lead Penetration" in the datasets.
    
    Return python code that answers the following user question:
    <<{user_instructions}>>
    """
    
def get_instructions_data_interpretation(user_query: str, query_results:str) -> str:
    return f"""
    {INTERPRET_DATA_PROMPT}
    
    User query:
    <<{user_query}>>
    
    Query results:
    <<{query_results}>>
    
    To help you better understand the context of the questions being asked here are some business terminology and definitions:
    <<{get_data_from_file(BUSINESS_DEFINITIONS_PATH)}>>
    
    Additionally, here are the summaries for the current datasets available:
    ORDERS:
    <<
    {get_data_from_file(SUMMARY_ORDERS_PATH)}
    >>
    The data frame for the orders dataset is called "df_orders". Use it as reference when creating the code.
    
    METRICS:
    <<
    {get_data_from_file(SUMMARY_METRICS_PATH)}
    >>
    """