def limit_input_range(func):
    def wrapper(*args, **kwargs):
        new_args = [min(max(0, arg), 5) if isinstance(arg, (int, float)) else arg for arg in args]
        new_kwargs = {k: min(max(0, v), 5) if isinstance(v, (int, float)) else v for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)
    return wrapper

@limit_input_range
def limited_add(num1, num2):
    return num1 + num2


# Test with arguments within and outside the range
print(limited_add(3,4))
print(limited_add(10,12))
print(limited_add(10,3))

