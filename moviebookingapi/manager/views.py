from flask import Blueprint, render_template, request, redirect, send_file
from ..services import BookingService, ShowService
from ..token import authenticate
from pony import orm
import xlsxwriter
import platform
import os

blueprint = Blueprint("manager", __name__, url_prefix="/manager")

@blueprint.route("/")
@orm.db_session
def manager():
    token = request.cookies.get('auth')

    if token:
        auth = authenticate(token)

        if auth[0]:
            user = auth[1]

            if user.manager:
                result = ShowService.list_shows()
                return render_template(
                    "views/manager.html",
                    shows=result
                )
            else:
                return redirect("/")

        else:
            return redirect("/login")

    else:
        return redirect("/login")


@blueprint.route("/download")
@orm.db_session
def download():
    path = "moviebookingapi/static/excel/" if platform.system().lower() == "linux" else "moviebookingapi\\static\\excel\\"
    excel_sheet = os.path.abspath(path) + "/test1.xlsx" if platform.system().lower() == "linux" else "\\test1.xlsx"
    print(excel_sheet)
    workbook = xlsxwriter.Workbook(excel_sheet)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for booking in BookingService.list_bookings():
        worksheet.write(row, col, booking.user.name)
        worksheet.write(row, col + 1, booking.show)
        worksheet.write(row, col + 2, booking.cost)
        row += 1

    workbook.close()

    return send_file(excel_sheet, as_attachment=True)
