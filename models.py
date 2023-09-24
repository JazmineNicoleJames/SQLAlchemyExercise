"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User model. """
    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String,
                            nullable = False)
    last_name = db.Column(db.String,
                            nullable = False)
    image_url = db.Column(db.String,
                            nullable = True)
    posts = db.relationship('Post', backref = 'user')

class Post(db.Model):
    """ Post model. """
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    title = db.Column(db.Text,
                    nullable = False)
    content = db.Column(db.Text,
                        nullable = False)
    created_at = db.Column(db.DateTime(timezone=True),
                            nullable = False,
                            default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))


    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class PostTag(db.Model):

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'), 
                        nullable = False,
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        nullable = False,
                        primary_key = True)



class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                    primary_key = True)
    name = db.Column(db.Text,
                    nullable = False,
                    unique = True)

    posts = db.relationship(
        'Post',
        secondary="post_tags",
        backref="tags"
    )



    
