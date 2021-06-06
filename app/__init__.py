from flask import Flask, render_template
from flask_login import LoginManager
from flask_admin import Admin

from . import models
from .blueprints import app as bp_app, colonies, users
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
app.register_blueprint(bp_app.bp)
app.register_blueprint(colonies.bp)
app.register_blueprint(users.bp)

# Register error pages
app.register_error_handler(401, lambda e: (render_template('errors/401.html'), 401)) # Unauthorized
app.register_error_handler(404, lambda e: (render_template('errors/404.html'), 404)) # Page not found

# Initialize administration and login mechanism
login_manager = LoginManager(app)
admin = Admin(app, index_view=AdminIndex())
admin_views(admin)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)