from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin

from . import models, routes_functions
from .admin import AdminIndex, admin_views
from config import Config

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)

# Create database
models.db.init_app(app)
app.app_context().push()
models.db.create_all()

# Register blueprints
from . import routes, routes_colony, routes_user # I know that it should not be in that place, but if i move it on the top "No application found".
app.register_blueprint(routes.bp)
app.register_blueprint(routes_colony.bp)
app.register_blueprint(routes_user.bp)

# Register error pages
app.register_error_handler(404, routes_functions.page_not_found)
app.register_error_handler(401, routes_functions.unauthorized)

# Initialize administration and login mechanism
login_manager = LoginManager(app)
admin = Admin(app, index_view=AdminIndex())
admin_views(admin)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)