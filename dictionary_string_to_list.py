def to_list(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            return list(result.items())
        elif isinstance(result, str):
            return list(result)
        else:
            return result
    return wrapper

@to_list
def return_dict():
    return {"a": 1, "b": 2, "c": 3}

@to_list
def return_string():
    return "hello"

print(return_dict()) 
print(return_string())  