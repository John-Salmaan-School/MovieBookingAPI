from flask import Flask, render_template, request, redirect
from .services import UserService, ShowService
from .auth.utils import hashpwd
from .token import authenticate
from pony import orm


def init_app():
    app = Flask(__name__)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    @app.route("/")
    @orm.db_session
    def index():
        token = request.cookies.get("auth")
        auth = authenticate(token)
        if not token or not auth[0]:
            return render_template("index.html")
        user = auth[1]
        if user.manager:
            return redirect("/manager")
        elif user.admin:
            return redirect("/admin")
        else:
            return render_template("index.html")


    @app.route("/remove")
    @orm.db_session
    def remove():
        token = request.cookies.get("auth")
        auth = authenticate(token)
        if not token or not auth[0]:
            return render_template("remove.html")
        user = auth[1]
        if user.manager:
            return redirect("/manager")
        elif user.admin:
            return redirect("/admin")
        else:
            return render_template("remove.html")

    @app.route("/update")
    @orm.db_session
    def update():
        token = request.cookies.get("auth")
        auth = authenticate(token)
        if not token or not auth[0]:
            return render_template("update.html")
        user = auth[1]
        if user.manager:
            return redirect("/manager")
        elif user.admin:
            return redirect("/admin")
        else:
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
        from .manager import manager
        from .view import view
        from .auth import auth
        from .show import show
        from .admin import admin

        app.register_blueprint(booking)
        app.register_blueprint(view)
        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(show)
        app.register_blueprint(manager)
        app.register_blueprint(admin)

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

    if not ShowService.get_show(name="Andwele"):
        ShowService.create(
            name="Andwele", cost_child=7, cost_adult=10,
            image="Andwele.png"
        )
