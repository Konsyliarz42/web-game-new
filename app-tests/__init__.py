from flask_testing import TestCase
from flask_login import login_user

from app import app as flask_app
from app.models import db, User, Colony, Buildings, Resources
from app.assets import buildings as constructions, tools, soldiers

TESTER = {
    'username': 'tester',
    'email': 'tester@tester.com',
    'password': 'xxxxxxxxx',
    'colony_name': 'TesterColony'
}

class MyTestCase(TestCase):

    def create_app(self):

        flask_app.config['TESTING'] = True
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.config['LOGIN_DISABLED'] = True

        db.session.remove()
        db.drop_all()

        return flask_app

    
    def setUp(self):

        db.create_all()

        tester = User(
            admin=True,
            username=TESTER['username'],
            email=TESTER['email']
        )
        tester.set_password(TESTER['password'])

        tester_colony = Colony(
            name=TESTER['colony_name'],
            owner_id=1
        )

        db.session.add(tester)
        db.session.add(tester_colony)
        db.session.commit()


    def tearDown(self):

        db.session.remove()
        db.drop_all()