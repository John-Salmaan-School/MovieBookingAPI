from ..services import BookingService
from flask import Blueprint
from pony import orm

blueprint = Blueprint("view", __name__, url_prefix="/view/")

@blueprint.route("/bookings", methods=["GET"])
@orm.db_session
def bookings():
    result = {"data": BookingService.list_bookings()}

    return result

@blueprint.route("/booking/<string:name>", methods=["GET"])
@orm.db_session
def booking(name):
    result = {"data": BookingService.get_booking(name)}

    return result
