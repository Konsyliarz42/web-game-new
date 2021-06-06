from unittest.mock import patch

from . import MyTestCase, TESTER, User, Colony, Buildings, Resources

class ColoniesTests(MyTestCase):

    # Show all pages in blueprint
    def test_show_pages(self):

        with patch('app.routes_functions.current_user') as mock_user:
            mock_user.colonies = Colony.query.all()

            # Create colony
            response = self.client.get('/colony/create')
            self.assertEqual(response.status_code, 200)

            # Status of colony
            response = self.client.get('/colony/1/status')
            self.assertEqual(response.status_code, 200)

            # Constructions of colony
            response = self.client.get('/colony/1/constructions')
            self.assertEqual(response.status_code, 200)


    # Create colony
    def test_create_colony(self):

        data = {'name': "TestColony"}

        with patch('app.routes_functions.current_user') as mock_user:
            mock_user.id = 1

            response = self.client.post('/colony/create', data=data)
            self.assertEqual(response.status_code, 302)


    # Create colony - Bad name
    def test_create_colony_bad_name(self):

        names = ['x', 'xx', 'x'*200, TESTER['colony_name']]

        with patch('app.routes_functions.current_user') as mock_user:
            mock_user.id = 1

            for name in names:
                response = self.client.post('/colony/create', data={'name': name})
                self.assertEqual(response.status_code, 400)


    # Start and abort build
    def test_constructions(self):

        with patch('app.routes_functions.current_user') as mock_user:
            mock_user.colonies = Colony.query.all()

            # Start 
            response = self.client.post('/colony/1/constructions', data={'construction': "sawmill"})
            self.assertEqual(response.status_code, 201)
            self.assertTrue(Colony.query.first().construction_list)

            # Abort
            response = self.client.post('/colony/1/status', data={'abort': "sawmill"})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(Colony.query.first().construction_list)


    # Start and abort build multiple constructions
    def test_constructions_multiple(self):

        with patch('app.routes_functions.current_user') as mock_user:
            mock_user.colonies = Colony.query.all()

            # Start build
            key = 'construction'
            url = '/colony/1/constructions'
            buildings = ['sawmill', 'quarry', 'farm']

            for _ in range(2):
                for building in buildings:
                    # Get colony before send request
                    colony = Colony.query.first()
                    resources = colony.resources.get_resources()
                    construction_list = colony.construction_list

                    self.client.post(url, data={key: building})
                    colony = Colony.query.first()

                    # Check resources and construction list
                    self.assertNotEqual(resources, colony.resources.get_resources()) 
                    self.assertNotEqual(construction_list, colony.construction_list)
                    
                    # Check time
                    if len(colony.construction_list) > 1:
                        end_time = colony.construction_list[-2].end_build
                        start_time = colony.construction_list[-1].start_build

                        self.assertEqual(end_time, start_time)

                # Abort build data
                key = 'abort'
                url = '/colony/1/status'
                buildings.reverse()