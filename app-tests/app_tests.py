from flask_login import current_user

from . import MyTestCase, TESTER

class AppTests(MyTestCase):
    
    # Show all pages in blueprint
    def test_show_pages(self):

        # Home
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

        # Auth
        response = self.client.get('/auth')
        self.assertEqual(response.status_code, 200)


    # Register, login and logout user
    def test_register_login_logout(self):

        data = {
            'username': 'TestUser',
            'email': 'test@test.com',
            'password': 'xxxxxxxxxx',
            'confirm_password': 'xxxxxxxxxx'
        }

        with self.client:
            # Register
            data['form'] = 'register'
            response = self.client.post('/auth', data=data)
            self.assertEqual(response.status_code, 201)

            # Login
            data['form'] = 'login'
            self.client.post('/auth', data=data)
            self.assertTrue(current_user.is_authenticated)

            # Logout
            self.client.post('/home')
            self.assertFalse(current_user.is_authenticated)

    # ================ R E G I S T E R   E R R O R S ================ 

    # Register - Empty field
    def test_register_empty_field(self):

        data = {
            'username': 'TestUser',
            'email': 'test@test.com',
            'password': 'xxxxxxxxxx',
            'confirm_password': 'xxxxxxxxxx'
        }

        for key in data.copy():
            _data = data.copy()
            _data[key] = ''
            _data['form'] = 'register'

            response = self.client.post('/auth', data=_data)
            self.assertEqual(response.status_code, 400)

    
    # Register - Bad username
    def test_register_bad_username(self):

        data = {
            'email': 'test@test.com',
            'password': 'xxxxxxxxxx',
            'confirm_password': 'xxxxxxxxxx',
            'form': 'register'
        }
        usernames = ['Y', 'YY', 'Y'*200, TESTER['username']]

        for username in usernames:
            data['username'] = username
            response = self.client.post('/auth', data=data)
            self.assertEqual(response.status_code, 400)


    # Register - Bad e-mail
    def test_register_bad_email(self):

        data = {
            'username': 'TestUser',
            'password': 'xxxxxxxxxx',
            'confirm_password': 'xxxxxxxxxx',
            'form': 'register'
        }
        emails = ['test@test', 'test.com', '@test.com', 'test@.com', TESTER['email']]

        for email in emails:
            data['email'] = email
            response = self.client.post('/auth', data=data)
            self.assertEqual(response.status_code, 400)


    # Register - Bad password
    def test_register_bad_password(self):

        data = {
            'username': 'TestUser',
            'email': 'test@test.com',
            'form': 'register'
        }
        passwords = ['x', 'xxxx', 'x'*300]

        for password in passwords:
            data['password'] = password
            data['confirm_password'] = password
            response = self.client.post('/auth', data=data)
            self.assertEqual(response.status_code, 400)


    # Register - Password not confirmed
    def test_register_password_not_confirmed(self):

        data = {
            'username': 'TestUser',
            'email': 'test@test.com',
            'password': 'xxxxxxxxxx',
            'confirm_password': 'xxxxxxxxxxY',
            'form': 'register'
        }

        response = self.client.post('/auth', data=data)
        self.assertEqual(response.status_code, 400)

    # ================ L O G I N   E R R O R S ================ 

    # Login - Empty field
    def test_login_empty_field(self):

        data = {
            'email': TESTER['email'],
            'password': TESTER['password'],
        }

        for key in data.copy():
            _data = data.copy()
            _data[key] = ''
            _data['form'] = 'login'

            response = self.client.post('/auth', data=_data)
            self.assertEqual(response.status_code, 400)


    # Login - Bad e-mail
    def test_login_bad_email(self):

        data = {
            'password': 'xxxxxxxxxx',
            'form': 'login'
        }
        emails = ['test@test', 'test.com', '@test.com', 'test@.com', 'x' + TESTER['email']]

        for email in emails:
            data['email'] = email
            response = self.client.post('/auth', data=data)
            self.assertEqual(response.status_code, 400)


    # Login - Bad password
    def test_login_bad_password(self):

        data = {
            'email': TESTER['email'],
            'form': 'login'
        }
        passwords = ['x', 'xxxx', 'x'*300, TESTER['password'] + 'Y']

        for password in passwords:
            data['password'] = password
            response = self.client.post('/auth', data=data)
            self.assertEqual(response.status_code, 400)
            