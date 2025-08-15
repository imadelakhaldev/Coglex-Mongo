"""
execution service routes module
the routes handle function execution functionality

this module provides routing rules and endpoints for execution operations including:
- function execution
"""


# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing base config parameters, and generic utilities
import config
from coglex import protected

# importing blueprint utilities used in current routing context
from coglex.services.execution.utils import execute


# blueprint instance
execution = Blueprint("execution", config.APP_IMPORT)


# function execution route
@execution.route("/service/execution/v1/execute/<function_name>/", methods=["POST"])
@execution.route("/service/execution/v1/execute/<function_name>", methods=["POST"])
@protected
def execution_execute(function_name: str):
    """
    handle function execution requests for a specified function name

    args:
        function_name (str): the name of the function to execute
    """
    # parsing request arguments
    args = request.json.get("args", [])
    kwargs = request.json.get("kwargs", {})

    try:
        # executing function
        result = execute(function_name, *args, **kwargs)
    except AttributeError as ex:
        # rethrow exception
        return abort(400, description=str(ex))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # returning results
    return jsonify(result), 200
