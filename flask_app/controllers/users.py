from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import user
from flask_app.models import recipe

#Create Route Controller 
@app.route("/create/user", methods=["POST"])
def creating_user():
    if user.User.create_user(request.form):
        return redirect('/users/dashboard')
    return redirect ("/")

#Read Route Controller
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/users/dashboard")
def user_dashboard():
    this_user = user.User.get_user_by_id(session['user_id'])
    all_user_recipes = recipe.Recipe.get_all_recipes_with_user()
    return render_template("dashboard.html" , this_user=this_user, all_user_recipes=all_user_recipes)

@app.route("/users/login", methods=['POST'])
def login(): 
    if user.User.login(request.form): 
        return redirect("/users/dashboard")
    return redirect('/')
    
#Update Route Controller

#Delete Route Controller 
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
