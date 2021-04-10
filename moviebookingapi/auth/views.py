from .args import login_args, register_args
from webargs.flaskparser import use_args
from .utils import checkpwd, hashpwd
from ..services import UserService
from flask import Blueprint
from pony import orm

blueprint = Blueprint("auth", __name__, url_prefix="/auth/")

@blueprint.route("/register", methods=["POST"])
@use_args(register_args, location="json")
@orm.db_session
def register(args):
    result = {"error": None}
    if UserService.get_by_email(args["email"]):
        result["error"] = "An account under that email exists. Please login"
        return result

    UserService.create(
        name=args["name"], email=args["email"], password=hashpwd(args["password"]),
        phone_num=args["phone_num"], admin=args["admin"]
    )
    return result

