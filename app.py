"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post, datetime
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

@app.route('/user_details/<int:user_id>/posts')
def add_post(user_id):
    users = User.query.get_or_404(user_id)

    return render_template('posts.html', users=users)


@app.route('/user_details/<int:user_id>/posts', methods=['POST'])
def submit_post(user_id):
    users = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']

    add_post = Post(title=title, content=content, user=users)

    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^__________')
    print(add_post.title)
    print(add_post.id)
    db.session.add(add_post)
    db.session.commit()
    flash(f"Post '{add_post.title}' added.")

    return redirect(f"/user_details/{user_id}")
    
@app.route('/post_details/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('/post_details.html', post_id = post_id, post=post)


@app.route('/post_details/<int:post_id>/edit_post')
def edit_post_route(post_id):
    post = Post.query.get_or_404(post_id)
    
    return render_template('edit_post.html', post = post)


@app.route('/post_details/<int:post_id>/edit_post', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    print('******************************************************************')
    print(post.title)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/user_details/{post.user_id}")


@app.route('/post_details/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/user_details/{post.user_id}")