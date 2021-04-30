from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename
from webargs.flaskparser import use_args
from ..services import ShowService
from ..token import authenticate
from .utils import allowed_file
from pony import orm
import platform
import os

blueprint = Blueprint("show", __name__, url_prefix="/show/")

@blueprint.route("/add", methods=["POST"])
@orm.db_session
def add():
    auth = authenticate(request.cookies.get("auth"))

    if auth[0]:
        user = auth[1]

        if user.manager:
            file = request.files['file']
            name = request.form['show_name']
            cost_child = request.form['cost_child']
            cost_adult = request.form['cost_adult']

            allowed_ext = ["png"]
            path = "moviebookingapi/static/img" if platform.system().lower() == "linux" else "moviebookingapi\\static\\img"
            upload_folder = os.path.abspath(path)

            if 'file' not in request.files:
                return render_template(
                    "views/show.html",
                    result="No file parameter in request"
                )

            if file.filename == "":
                return render_template(
                    "views/show.html",
                    result="No selected file"
                )

            if file and allowed_file(filename=file.filename, ext_list=allowed_ext):
                filename = secure_filename(name + ".png")
                path = os.path.join(upload_folder, filename)
                if os.path.exists(path):
                    return render_template(
                        "views/show.html",
                        result="Show already exists"
                    )
                ShowService.create(
                    name=name, cost_child=cost_child,
                    cost_adult=cost_adult, image=file.filename
                )
                file.save(path)
                return render_template(
                    "views/show.html",
                    result="Show added successfully"
                )
            else:
                return render_template(
                    "views/show.html",
                    result="File format is incorrect"
                )

        else:
            return render_template(
                "views/show.html",
                result="You don't have permission to do this"
            )

    else:
        return render_template(
            "views/show.html",
            result=auth[1]
        )

@blueprint.route("/get/<string:name>", methods=["GET"])
@orm.db_session
def get(name):
    result = {"data": {}, "error": None}
    auth = authenticate(request.headers.get("Authentication"))
    show = ShowService.get_show(name=name)

    if auth[0]:

        if show:
            result["data"] = {
                "name": show.name,
                "cost_adult": show.cost_adult,
                "cost_child": show.cost_child,
                "image": show.image
            }

            return result
        else:
            result["error"] = "Show doesn't exist"

    else:
        result["error"] = auth[1]
        return result


@blueprint.route("/update", methods=["POST"])
@orm.db_session
def update():
    auth = authenticate(request.cookies.get("auth"))

    if auth[0]:
        user = auth[1]

        if user.manager:
            print(request.files['file'].filename)
            file = request.files['file'] if request.files['file'].filename != "" else None
            name = request.form['show_name']
            cost_child = request.form['cost_child']
            cost_adult = request.form['cost_adult']

            allowed_ext = ["png"]
            path = "moviebookingapi/static/img" if platform.system().lower() == "linux" else "moviebookingapi\\static\\img"
            upload_folder = os.path.abspath(path)
            show = ShowService.get_show(name=name)

            if file is not None:
                if show.image != file.filename:
                    if 'file' not in request.files:
                        return render_template(
                            "views/show.html",
                            result="No file parameter in request"
                        )

                    if file.filename == "":
                        return render_template(
                            "views/show.html",
                            result="No selected file"
                        )

                    if allowed_file(filename=file.filename, ext_list=allowed_ext):
                        filename = secure_filename(name + ".png")
                        path = os.path.join(upload_folder, filename)
                        file.save(path)

                        ShowService.update(
                            name=name, cost_child=cost_child,
                            cost_adult=cost_adult, image=filename
                        )
                        return render_template(
                            "views/show.html",
                            result="Show updated successfully"
                        )
            else:
                ShowService.update(
                    name=name, cost_child=cost_child,
                    cost_adult=cost_adult, image=show.image
                )
                return render_template(
                    "views/show.html",
                    result="Show updated successfully"
                )

        else:
            render_template(
                "views/show.html",
                result=auth[1]
            )



@blueprint.route("/remove/<string:name>", methods=["POST"])
@orm.db_session
def remove(name):
    result = {"error": None}
    auth = authenticate(request.headers.get("Authentication"))

    if auth[0]:
        user = auth[1]

        if user.manager:

            if not ShowService.get_show(name=name):
                result["error"] = "Show does not exist"
                return result

            ShowService.remove(name)

            path = f"moviebookingapi/static/img/{name}.png" if platform.system().lower() == "linux" else f"moviebookingapi\\static\\img\\{name}.png"
            upload_folder = os.path.abspath(path)

            try:
                os.remove(upload_folder)
            except FileNotFoundError:
                pass

            return result
        else:
            result["error"] = "You do not have permission to do this"
            return result

    else:
        result["error"] = auth[1]
        return result

@blueprint.route("/list", methods=["GET"])
@orm.db_session
def list():
    result = {"shows": []}
    for show in ShowService.list_shows():
        result["shows"].append(show.name)

    return result
