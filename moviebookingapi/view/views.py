from flask import Blueprint, render_template, request, redirect
from ..services import BookingService, UserService
from ..token import authenticate
from pony import orm

blueprint = Blueprint("view", __name__, url_prefix="/view/")

@blueprint.route("/bookings", methods=["GET"])
@orm.db_session
def bookings():
    token = request.cookies.get('auth')
    result = {"error": None}

    if token:
        auth = authenticate(token)

        if auth[0]:
            user = auth[1]

            if user.manager:
                result = BookingService.list_bookings()
                return render_template(
                    "views/bookings.html",
                    bookings=result
                )
            else:
                result = user.bookings.select()
                return render_template(
                    "views/bookings.html",
                    bookings=result
                )
        else:
            result["error"] = auth[1]
            return result
    else:
        return redirect("/login")

@blueprint.route("/booking/<string:bid>", methods=["GET"])
@orm.db_session
def booking(bid):
    token = request.cookies.get('auth')
    result = {"error": None}

    if token:
        auth = authenticate(token)

        if auth[0]:
            user = auth[1]

            if user.manager:
                result = BookingService.get_booking(bid=bid)
                return render_template(
                    "views/booking.html",
                    booking=result
                )
            else:
                bookings = user.bookings.select(lambda x: x.bid == bid)
                result = None
                for booking in bookings:
                    result = booking
                return render_template(
                    "views/booking.html",
                    booking=result
                )
        else:
            result["error"] = auth[1]
            return result
    else:
        return redirect("/login")

@blueprint.route("/users", methods=["GET"])
@orm.db_session
def users():
    token = request.cookies.get('auth')
    result = {"error": None}

    if token:
        auth = authenticate(token)
        if auth[0]:
            user = auth[1]

            if user.admin:
                result = UserService.list_users()
                return render_template(
                    "views/users.html",
                    users=result
                )
            else:
                result["error"] = "You do not have the required permissions"
                return result
        else:
            result["error"] = auth[1]
            return result
    else:
        return redirect("/login")
