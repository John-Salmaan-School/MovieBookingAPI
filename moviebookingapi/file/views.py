from flask import Blueprint, request, render_template, redirect
from werkzeug.utils import secure_filename
from ..utils import allowed_file
from ..token import authenticate
import platform
import os

blueprint = Blueprint("file", __name__, url_prefix="/file/")

@blueprint.route("/upload", methods=["POST", "GET"])
def upload():
    allowed_ext = ["png"]
    path = "moviebookingapi/static/img" if platform.system().lower() == "linux" else "moviebookingapi\\static\\img"
    upload_folder = os.path.abspath(path)

    if request.method == "POST":
        result = {"error": None}
        if 'file' not in request.files:
            result["error"] = "No file parameter in request"
            return result

        file = request.files['file']
        name = request.form["filename"]

        if file.filename == "":
            result["error"] = "No selected file"
            return result

        if file and allowed_file(filename=file.filename, ext_list=allowed_ext):
            filename = secure_filename(name + ".png")
            path = os.path.join(upload_folder, filename)
            file.save(path)
            return result
        else:
            result["error"] = "File format is incorrect"
            return result

    auth = authenticate(request.cookies.get("auth"))

    if not auth[0]:
        return redirect("/")
    else:
        user = auth[1]

        if user.manager:
            return render_template("upload.html")
        else:
            return redirect("/")
