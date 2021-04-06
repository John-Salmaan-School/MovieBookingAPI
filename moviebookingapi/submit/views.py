from webargs.flaskparser import use_args
from ..services import BookingService
from flask import Blueprint
from .args import submit_args
from pony import orm

blueprint = Blueprint("submit", __name__)

@blueprint.route("/submit", methods=["POST"])
@use_args(submit_args, location="json")
@orm.db_session
def submit(args):

    result = {"data": {
        "name": args["name"],
        "show": args["show"],
        "date": args["date"],
        "adult": args["adult_tickets"],
        "child": args["child_tickets"],
        "discount": args["discount"],
        "cost": args["cost"]
    }}

    BookingService.create(
        name=args["name"], show=args["show"],
        date=args["date"], adult_num=args["adult_tickets"],
        child_num=args["child_tickets"], discount=args["discount"],
        cost=args["cost"]
    )

    return result
