from .args import submit_args, remove_args, update_args
from webargs.flaskparser import use_args
from ..services import BookingService
from flask import Blueprint, request
from .utils import gen_booking_id
from ..token import authenticate
from pony import orm

blueprint = Blueprint("booking", __name__, url_prefix="/booking/")

@blueprint.route("/submit", methods=["POST"])
@use_args(submit_args, location="json")
@orm.db_session
def submit(args):
    result = {"id": "", "error": None}
    auth = authenticate(request.headers.get("Authentication"))

    if auth[0]:
        user = auth[1]

        bid = gen_booking_id()
        BookingService.create(
            bid=bid, user=user, show=args["show"],
            date=args["date"], adult_num=args["adult_tickets"],
            child_num=args["child_tickets"], discount=args["discount"],
            cost=args["cost"]
        )
        result["id"] = bid
        return result
    else:
        result["error"] = auth[1]
        return result

@blueprint.route("/remove", methods=["POST"])
@use_args(remove_args, location="json")
@orm.db_session
def remove(args):
    result = {"error": None}

    if BookingService.get_booking(args["id"]):
        BookingService.remove(bid=args["id"])

    else:
        result["error"] = "Booking does not exists under that ID"

    return result

@blueprint.route("/update", methods=["POST"])
@use_args(update_args, location="json")
@orm.db_session
def update(args):
    result = {"error": None}
    auth = authenticate(request.headers.get("Authentication"))
    booking = BookingService.get_booking(args["id"])

    if auth[0]:
        user = auth[1]

        if booking in user.bookings:
            BookingService.update(
                bid=args["id"], show=args["show"], date=args["date"],
                adult_num=args["adult_tickets"], child_num=args["child_tickets"],
                discount=args["discount"], cost=args["cost"]
            )
        else:
            result["error"] = "Booking doesn't exist under your account"

    else:
        result["error"] = auth[1]

    return result

@blueprint.route("/list", methods=["GET"])
@orm.db_session
# TODO: Auth Only for manager
def list():
    result = {"data": []}

    for booking in BookingService.list_bookings():
        booking_detail = {
            "id": booking.bid,
            "name": booking.user.name,
            "show": booking.show,
            "date": booking.date,
            "adult": booking.adult_num,
            "child": booking.child_num,
            "discount": booking.discount,
            "cost": booking.cost
        }

        result["data"].append(booking_detail)

    return result

@blueprint.route("/get/<string:bid>", methods=["GET"])
@orm.db_session
def get(bid):
    result = {"data": {}}

    booking = BookingService.get_booking(bid)
    result["data"] = {
        "id": booking.bid,
        "name": booking.user.name,
        "show": booking.show,
        "date": booking.date,
        "adult": booking.adult_num,
        "child": booking.child_num,
        "discount": booking.discount,
        "cost": booking.cost
    }

    return result

