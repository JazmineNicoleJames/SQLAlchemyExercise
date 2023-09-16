"""Blogly application."""

from flask import Flask, render_template, request, redirect, session
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def home_route():
    """ Show all users in db """
    users = User.query.all()
    
    return render_template('index.html', users=users)


@app.route('/create_user')
def create_user():

    return render_template('create_user.html')

@app.route('/create_user', methods=['POST'])
def submit_create_user():
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    image_url = request.form['image']  
    form = User(first_name=firstname, last_name=lastname, image_url = image_url)
    db.session.add(form)
    db.session.commit()
    print(request.form)

    return redirect(f'/user_details/{form.id}')


@app.route('/user_details/<int:user_id>')
def user_details(user_id):
    users = User.query.get(user_id)
    firstname = users.first_name
    lastname = users.last_name
    image_url = users.image_url

    return render_template('user_details.html', users=users, firstname = users.first_name, lastname= users.last_name, image_url = image_url)
        
@app.route('/user_details/<int:user_id>/edit_user')
def edit_user(user_id):
    users = User.query.get_or_404(user_id)

    return render_template('edit_user.html', users=users, user_id=user_id)


@app.route('/user_details/<int:user_id>/edit_user', methods=['POST'])
def user_update(user_id):
    users = User.query.get_or_404(user_id)
    users.first_name = request.form['first_name']
    users.last_name = request.form['last_name']
    users.image_url = request.form['image']  
    
    db.session.add(users)
    db.session.commit()

    return redirect(f'/user_details/{user_id}')


@app.route('/user_details/<int:user_id>/delete_user', methods=['POST'])
def delete_user(user_id):
    users = User.query.get_or_404(user_id)
    db.session.delete(users)
    db.session.commit()

    return redirect('/')