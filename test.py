from app import app
from unittest import TestCase

class BloglyTestCase(TestCase):


    def test_home_route(self):
        """ Test home route. """
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)

            self.assertIn('<h1> Users </h1>', html)
            self.assertEqual(res.status_code, 200)


    def test_create_user(self):
        """ Test create user. """
        with app.test_client() as client:
            res = client.post('/create_user', 
            data = dict(first_name = 'Jaz',
                        last_name = 'James',
                        image = 'https://en.m.wikipedia.org/wiki/File:Sunflower_from_Silesia2.jpg'),
                        follow_redirects=True)

            self.assertEqual(res.status_code, 200)


    def test_edit_user(self):
        """ Test edit user. """
        with app.test_client() as client:
            res = client.get('/user_details/48/edit_user',
            data = dict(first_name = 'Jaz',
                        last_name = 'James',
                        image_url = 'https://en.m.wikipedia.org/wiki/File:Sunflower_from_Silesia2.jpg'),
                        follow_redirects=True)

            self.assertEqual(res.status_code, 200)

    def test_delete_user(self):
        """ Test deleting a user. """
        with app.test_client() as client:
            res = client.post('/user_details/49/delete_user',
            data = dict(first_name = 'Jaz',
                        last_name = 'James',
                        image_url = 'https://en.m.wikipedia.org/wiki/File:Sunflower_from_Silesia2.jpg'),
                        follow_redirects=True)
                        
            self.assertEqual(res.status_code, 200)
        