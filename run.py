"""
server deployment, execution, and serving module
this module serves as the project entry point for running the wsgi server in both development and production environments
"""


# pip install waitress
# lightweight wsgi production server deployment
from waitress import serve

# importing global config parameters, and generic utilities
import config
from utils import sprint

# importing application object to run
from coglex import application


# application entry point
if __name__ == "__main__":
    try:
        # development server flag activated
        if config.SERVER_DEBUG:
            # serving development server
            application.run(host=config.SERVER_HOST, port=config.SERVER_PORT, debug=config.SERVER_DEBUG)

        # production server flag activated
        if not config.SERVER_DEBUG:
            # serving production server
            serve(application, host=config.SERVER_HOST, port=config.SERVER_PORT)
    except Exception as ex:
        # printing failures
        sprint("RED", str(ex))
