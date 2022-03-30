from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user
from app import app, session
from datetime import timedelta
from app.models.models import SlaUserManagement
from config import config

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = '/login'
login_manager.refresh_view = '/login'
login_manager.needs_refresh_message = u"Session timedout, please re-login"
login_manager.needs_refresh_message_category = "info"


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=int(config.SESSION_TIMEOUT))


@login_manager.user_loader
def load_user(user):
    return SlaUserManagement.query.get(user)
