from flask_login import LoginManager
from app.repositories.users import get_by_id


def init_login(app):
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        conn = app.config.get("DB_GETTER")()
        return get_by_id(conn, int(user_id))

    return login_manager
