import os

def get_env_variable(name:str, default_value:str = None) -> str:
    value:str = os.getenv(name)
    if  value == None:
        return default_value
    return value