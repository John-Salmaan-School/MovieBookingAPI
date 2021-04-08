from .args import submit_args, remove_args
from webargs.flaskparser import use_args
from ..services import BookingService
from flask import Blueprint
from pony import orm

blueprint = Blueprint("booking", __name__, url_prefix="/booking/")

@blueprint.route("/submit", methods=["POST"])
@use_args(submit_args, location="json")
@orm.db_session
def submit(args):
    result = {"error": None}

    if len(BookingService.get_booking(args["name"])) == 0:

        BookingService.create(
            name=args["name"], show=args["show"],
            date=args["date"], adult_num=args["adult_tickets"],
            child_num=args["child_tickets"], discount=args["discount"],
            cost=args["cost"]
        )

    else:
        result["error"] = "Booking already exists"

    return result

@blueprint.route("/remove", methods=["POST"])
@use_args(remove_args, location="json")
@orm.db_session
def remove(args):
    result = {"error": None}

    if not len(BookingService.get_booking(args["name"])) == 0:
        BookingService.remove(name=args["name"])

    else:
        result["error"] = "Booking does not exists under that name"

    return result

