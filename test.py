from app import app
from unittest import TestCase
from flask import Flask, request, redirect
from models import User, Post
from flask_sqlalchemy import SQLAlchemy
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly' 
db = SQLAlchemy(app)

class BloglyTestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        self.test_user = User(first_name='Test', last_name='User', image_url='test.jpg')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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
            data = dict(id = '50',
                first_name = 'Jaz',
                        last_name = 'James',
                        image = 'https://en.m.wikipedia.org/wiki/File:Sunflower_from_Silesia2.jpg'),
                        follow_redirects=True)

            self.assertEqual(res.status_code, 200)



    """ def test_delete_user(self):
        """ """ Test deleting a user. """"""
        res = self.app.delete(f'/user_details/{self.test_user.id}/delete_user', follow_redirects=True)
        self.assertEqual(res.status_code, 200)  """


    def test_edit_user(self):
        """ Test editing a user."""
        data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'image': 'updated.jpg'
        }

        response = self.app.post(f'/user_details/{self.test_user.id}/edit_user', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_submit_post(self):
        """ Test submitting a post."""
        with self.app as client:
            data = {
                'title': 'Hello',
                'content':'Hi'
            }
            response = client.post(f'/user_details/{self.test_user.id}/posts', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        