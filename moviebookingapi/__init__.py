from flask import Flask, render_template

def init_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    with app.app_context():
        from .submit import submit
        from .view import view

        app.register_blueprint(submit)
        app.register_blueprint(view)

        return app
