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
from coglex.services.execution.utils import _execute


# blueprint instance
_execution = Blueprint("_execution", config.APP_IMPORT)


# function execution route
@_execution.route("/service/execution/v1/execute/<function>/", methods=["POST"])
@_execution.route("/service/execution/v1/execute/<function>", methods=["POST"])
@protected()
def execute(function: str):
    """
    handle function execution requests for a specified function name

    args:
        function (str): the name of the function to execute
    """
    # parsing request arguments
    args, kwargs = request.json.get("args", []), request.json.get("kwargs", {})

    try:
        # executing function
        result = _execute(function, *args, **kwargs)
    except AttributeError as ex:
        # rethrow exception
        return abort(400, description=str(ex))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # returning results
    return jsonify(result), 200
