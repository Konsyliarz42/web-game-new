from . import app
from .admin import create_first_admin
from .models import User

if __name__ == '__main__':
    with app.app_context():
        if not User.query.filter_by(admin=True).all():
            create_first_admin()

    app.run(debug=True)