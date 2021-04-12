from ..services import BookingService, UserService
from flask import Blueprint, render_template
from pony import orm

blueprint = Blueprint("view", __name__, url_prefix="/view/")

@blueprint.route("/bookings", methods=["GET"])
@orm.db_session
def bookings():
    result = BookingService.list_bookings()

    return render_template(
        "views/bookings.html",
        bookings=result
    )

@blueprint.route("/booking/<string:bid>", methods=["GET"])
@orm.db_session
def booking(bid):
    result = BookingService.get_booking(bid=bid)

    return render_template(
        "views/booking.html",
        booking=result
    )

@blueprint.route("/users", methods=["GET"])
@orm.db_session
def users():
    result = UserService.list_users()

    return result
