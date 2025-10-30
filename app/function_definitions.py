function_schema_registry = {}

def register_function(function_definition:dict) -> None:
    function_schema_registry[function_definition["name"]] = function_definition


# *************** FUNCTIONS ***********************

add_two_numbers = {
    "name":"add_two_numbers",
    "description":"given two numbers it returns the resulting sum of adding them",
    "parameters":{
        "type":"object",
        "properties":{
            "num_1":{
                "type":"integer",
                "description":"first number to consider in the sum"
            },
            "num_2":{
                "type":"integer",
                "description":"second number to consider in the sum"
            }
        }
    }
}

register_function(add_two_numbers)


