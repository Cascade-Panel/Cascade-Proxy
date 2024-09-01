import logging
from sanic.response import json
from config import LOG_FILE_PATH

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.ERROR)

def setup_error_handlers(app):
    """
    Set up error handlers for the Sanic application.

    Args:
        app (Sanic): The Sanic application instance.
    """

    @app.exception(Exception)
    async def handle_exception(request, exception):
        """
        Handle unexpected exceptions.

        Args:
            request (Request): The request object.
            exception (Exception): The raised exception.

        Returns:
            Response: JSON response with error message.
        """
        logging.error(f"Unexpected error: {str(exception)}")
        return json({"error": "An unexpected error occurred"}, status=500)

    @app.exception(ValueError)
    async def handle_value_error(request, exception):
        """
        Handle ValueError exceptions.

        Args:
            request (Request): The request object.
            exception (ValueError): The raised ValueError.

        Returns:
            Response: JSON response with error message.
        """
        logging.error(f"ValueError: {str(exception)}")
        return json({"error": str(exception)}, status=400)