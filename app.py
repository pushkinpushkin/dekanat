from flask import Flask
from flask_login import login_required, current_user
from app.config import Config
from app.db import init_pool, close_db, get_db
from app.auth import init_login
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.students import students_bp
from app.routes.courses import courses_bp
from app.routes.gradebooks import gradebooks_bp
from app.routes.reports import reports_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_pool(app)
    app.config["DB_GETTER"] = get_db

    login_manager = init_login(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(gradebooks_bp)
    app.register_blueprint(reports_bp)

    @app.teardown_appcontext
    def teardown_db(exception=None):
        close_db()

    @app.context_processor
    def inject_user():
        return {"current_user": current_user}

    return app


app = create_app()


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
