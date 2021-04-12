from .args import login_args, register_args
from webargs.flaskparser import use_args
from .utils import checkpwd, hashpwd
from ..services import UserService
from flask import Blueprint
from ..token import Token
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
        phone_num=args["phone_num"], admin=args["admin"], manager=args["manager"]
    )
    return result

@blueprint.route("/login", methods=["POST"])
@use_args(login_args, location="json")
@orm.db_session
def login(args):
    result = {"data": {}, "error": None}

    user = UserService.get_by_email(args["email"])
    if not user:
        result["error"] = "Account does not exist under that email"
        return result

    if not checkpwd(args["password"], user.password):
        result["error"] = "Incorrect password. Please try again"
        return result

    token = Token.create("login", user.email)
    data = Token.payload(token)

    result["data"] = {
        "token": token,
        "expire": data["expire"],
        "email": data["meta"]
    }

    return result




