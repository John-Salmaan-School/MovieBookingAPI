from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from .utils import allowed_file
from path import Path
import platform
import os

def init_app():
    app = Flask(__name__)

    allowed_ext = ["png"]
    path = "moviebookingapi/static/img" if platform.system().lower() == "linux" else "moviebookingapi\\static\\img"
    upload_folder = os.path.abspath(path)

    app.config["UPLOAD_FOLDER"] = upload_folder

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/remove")
    def remove():
        return render_template("remove.html")

    @app.route("/update")
    def update():
        return render_template("update.html")

    @app.route("/register")
    def register():
        return render_template("register.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/upload", methods=["POST", "GET"])
    def upload():
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
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(path)
                return result
            else:
                result["error"] = "File format is incorrect"
                return result

        return render_template("upload.html")

    with app.app_context():
        from .booking import booking
        from .profile import profile
        from .view import view
        from .auth import auth

        app.register_blueprint(booking)
        app.register_blueprint(view)
        app.register_blueprint(auth)
        app.register_blueprint(profile)

        return app
