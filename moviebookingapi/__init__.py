from flask import Flask, render_template
from .services import UserService
from .auth.utils import hashpwd
from pony import orm


def init_app():
    app = Flask(__name__)

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

    with app.app_context():
        from .booking import booking
        from .profile import profile
        from .view import view
        from .auth import auth
        from .file import file

        app.register_blueprint(booking)
        app.register_blueprint(view)
        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(file)

        return app


@orm.db_session
def init_db():
    if not UserService.get_by_email(email="salmaan@salmaan.com"):
        UserService.create(
            name="Salmaan", email="salmaan@salmaan.com", password=hashpwd("salmaan1234"),
            phone_num="123456789", admin=True, manager=False
        )

    if not UserService.get_by_email("nagoormira@nagoormira.com"):
        UserService.create(
            name="Nagoormira", email="nagoormira@nagoormira.com", password=hashpwd("nagoormira1234"),
            phone_num="123456789", admin=False, manager=True
        )
