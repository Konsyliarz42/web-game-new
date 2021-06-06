from unittest.mock import patch

from . import MyTestCase, TESTER, User, Colony, Buildings, Resources

class UsersTests(MyTestCase):
    
    # Show all pages in blueprint
    def test_show_pages(self):

        # Profile
        with patch('app.blueprints.users.get_user') as mock_user:
            response = self.client.get('/user/1/profile')
            self.assertEqual(response.status_code, 200)


    # Delete colony
    def test_delete_colony(self):
        
        data = {
            'form': 'delete_colony',
            'id': '1'
        }

        with patch('app.blueprints.users.get_user') as mock_user:
            response = self.client.post('/user/1/profile', data=data)
            self.assertEqual(response.status_code, 200)

            self.assertFalse(Colony.query.all())
            self.assertFalse(Buildings.query.all())
            self.assertFalse(Resources.query.all())


    # Delete colony - Colony not exist
    def test_delete_colony_not_exist(self):
        
        data = {
            'form': 'delete_colony',
            'id': '2'
        }

        with patch('app.blueprints.users.get_user') as mock_user:
            response = self.client.post('/user/1/profile', data=data)
            self.assertEqual(response.status_code, 400)


    # Delete user
    def test_delete_user(self):
        
        data = {'form': 'delete_user'}

        with patch('app.blueprints.users.get_user') as mock_user:
            mock_user.return_value = User.query.first()

            with self.client:
                response = self.client.post('/user/1/profile', data=data)
                self.assertEqual(response.status_code, 302)

                self.assertFalse(User.query.all())
                self.assertFalse(Colony.query.all())
                self.assertFalse(Buildings.query.all())
                self.assertFalse(Resources.query.all())