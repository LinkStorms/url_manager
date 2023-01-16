from functools import wraps

from flask import Flask, json, request
from werkzeug.exceptions import HTTPException
from flasgger import Swagger, swag_from

from settings import HOST, PORT
from communications import (
    check_auth,
    create_short_url,
    delete_short_url,
    get_short_url_list,
)


app = Flask(__name__)
swagger = Swagger(app)


def is_authorized(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        auth_response = check_auth(authorization)
        if auth_response["code"] == 200:
            setattr(request, "user_id", auth_response["data"]["user_id"])
            return f(*args, **kwargs)
        else:
            return auth_response, auth_response["code"]
    return decorated_func


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        # "name": e.name,
        "data": {},
        "errors": [e.description],
    })
    response.content_type = "application/json"
    return response


@app.route("/create_short_url", methods=["POST"])
@swag_from("flasgger_docs/create_short_url_endpoint.yml")
@is_authorized
def create_short_url_endpoint():
    url = request.json.get("url", "")
    alias = request.json.get("alias", "")
    note = request.json.get("note", "")
    preferred_service = request.json.get("preferred_service", "")
    user_id = getattr(request, "user_id", "")

    response = create_short_url(user_id, url, alias, note, preferred_service)
    return response, response["code"]


@app.route("/delete_short_url", methods=["DELETE"])
@swag_from("flasgger_docs/delete_short_url_endpoint.yml")
@is_authorized
def delete_short_url_endpoint():
    short_url_id = request.args.get("short_url_id", "")
    user_id = getattr(request, "user_id", "")

    response = delete_short_url(user_id, short_url_id)
    return response, response["code"]


@app.route("/get_short_url_list", methods=["GET"])
@swag_from("flasgger_docs/get_short_url_list_endpoint.yml")
@is_authorized
def get_short_url_list_endpoint():
    user_id = getattr(request, "user_id", "")

    response = get_short_url_list(user_id)
    return response, response["code"]


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
