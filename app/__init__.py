from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

from . import models
from .admin import AdminIndex, admin_views
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

models.db.init_app(app)
migrate = Migrate(app, models.db)
app.app_context().push()

from . import routes # I know that it should not be in that place, but if i move it on the top "No application found".
app.register_blueprint(routes.bp)

login_manager = LoginManager(app)
admin = Admin(app, index_view=AdminIndex())
admin_views(admin)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)