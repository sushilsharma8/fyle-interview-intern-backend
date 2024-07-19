from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data=None, error=None, message=None, status_code=200):
        """
        Create a response with optional data and error message.

        :param data: The data to include in the response body (optional).
        :param error: The error message to include in the response body (optional).
        :param status_code: The HTTP status code for the response (default is 200).
        :return: A Flask response object.
        """
        response_content = {}
        if data is not None:
            response_content['data'] = data
        if error is not None:
            response_content['error'] = error
        if message is not None:
            response_content['message'] = message

        response = make_response(jsonify(response_content), status_code)
        return response
