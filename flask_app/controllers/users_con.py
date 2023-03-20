from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import users_mod
from flask_app.models import recipe_mod
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# *****LOGIN AND REG*****

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register', methods=["POST"])
def register():
    if not users_mod.Users.validate_user(request.form):
        return redirect('/')
    user_data= {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash (request.form['password'])}
    user_id = users_mod.Users.save(user_data)
    session['user_id'] = user_id 
    return redirect('/recipe/wall')

@app.route('/login', methods=['POST'])
def login():
    data = {'email':request.form['email']}
    user_in_DB = users_mod.Users.get_user_by_email(data)
    if not user_in_DB:
        flash('Invalid email','login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_DB.password,request.form['password']):
        flash('Incorrect Password or Email, try again','login')
        return redirect('/')
    session['id'] = user_in_DB.id
    session['first_name'] = user_in_DB.first_name
    session['email'] = user_in_DB.email
    return redirect('/recipe/wall')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')