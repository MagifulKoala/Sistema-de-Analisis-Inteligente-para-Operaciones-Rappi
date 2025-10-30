function_definition_registry = {}

def register_function(func):
    function_definition_registry[func.__name__] = func
    
def execute_function(function_name:str, args):
    return function_definition_registry[function_name](**args)

# ************* functions ********************

def add_two_numbers(num_1: int, num_2: int) -> int:
    return num_1 + num_2
register_function(add_two_numbers)

def subtract_two_numbers(num_1: int, num_2: int) -> int:
    return num_1 - num_2
register_function(subtract_two_numbers)

def give_the_anser_to_everything(question: str) -> int:
    return 42
register_function(give_the_anser_to_everything)