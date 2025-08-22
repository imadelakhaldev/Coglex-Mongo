"""
execution service module for managing function execution operations
this module provides functionality for dynamic function execution from the main utils.py
"""

# retrieve information from live Python objects.
import inspect


def execute(function_name: str, *args, **kwargs) -> any:
    """
    dynamically loads and executes a function from the main utils.py file

    args:
        function_name (str): the name of the function to execute
        *args: positional arguments to pass to the function
        **kwargs: keyword arguments to pass to the function

    returns:
        any: the result of the executed function
    """
    try:
        # get the function from the current module's globals
        func = globals().get(function_name)

        # check if the found object is a callable function defined in this module
        if not (inspect.isfunction(func) and func.__module__ == __name__):
            if func is None or not callable(func):
                raise AttributeError(f"Failure Calling Function '{function_name}' in 'utils.py'")

        # execute the function with provided arguments
        return func(*args, **kwargs)
    except Exception as ex:
        # rethrow exception
        raise ex


def example_function(name: str, greeting: str = "Hello"):
    """
    An example function to demonstrate execution.
    """
    return f"{greeting}, {name}! This function is from execution/utils.py."
