from flask import Flask, render_template

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

    with app.app_context():
        from .booking import booking
        from .view import view

        app.register_blueprint(booking)
        app.register_blueprint(view)

        return app
