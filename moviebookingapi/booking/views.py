from .args import submit_args, remove_args, update_args
from webargs.flaskparser import use_args
from ..services import BookingService
from .utils import gen_booking_id
from flask import Blueprint
from pony import orm

blueprint = Blueprint("booking", __name__, url_prefix="/booking/")

@blueprint.route("/submit", methods=["POST"])
@use_args(submit_args, location="json")
@orm.db_session
def submit(args):
    result = {"id": "", "error": None}

    if len(BookingService.get_booking_by_name(args["name"])["data"]) == 0:

        bid = gen_booking_id()
        BookingService.create(
            bid=bid, name=args["name"], show=args["show"],
            date=args["date"], adult_num=args["adult_tickets"],
            child_num=args["child_tickets"], discount=args["discount"],
            cost=args["cost"]
        )

        result["id"] = bid

    else:
        result["error"] = "Booking already exists under that name"

    return result

@blueprint.route("/remove", methods=["POST"])
@use_args(remove_args, location="json")
@orm.db_session
def remove(args):
    result = {"error": None}

    if not len(BookingService.get_booking(args["id"])) == 0:
        BookingService.remove(bid=args["id"])

    else:
        result["error"] = "Booking does not exists under that ID"

    return result

@blueprint.route("/update", methods=["POST"])
@use_args(update_args, location="json")
@orm.db_session
def update(args):
    result = {"error": None}

    if not len(BookingService.get_booking(args["id"])) == 0:
        BookingService.update(
            bid=args["id"], show=args["show"], date=args["date"],
            adult_num=args["adult_tickets"], child_num=args["child_tickets"],
            discount=args["discount"], cost=args["cost"]
        )

    else:
        result["error"] = "Booking does not exist under that ID"

    return result

