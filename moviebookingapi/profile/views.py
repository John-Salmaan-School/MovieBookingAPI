from flask import request, Blueprint
from ..token import authenticate

blueprint = Blueprint("profile", __name__, url_prefix="/profile/")

@blueprint.route("/info", methods=["GET"])
def info():
    result = {"data": {}, "error": None}
    auth = authenticate(request.headers.get("Authentication"))

    if auth[0]:
        user = auth[1]
        result["data"] = {
            "name": user.name,
            "admin": user.admin,
            "manager": user.manager
        }
        return result
    else:
        result["error"] = auth[1]
        return result
