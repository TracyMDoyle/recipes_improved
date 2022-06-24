from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import recipe 
from flask_app.models import user 

#create recipes
@app.route('/recipes/create')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template("new.html", this_user=this_user)

@app.route('/recipes/add', methods=['POST'])
def adding_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if recipe.Recipe.create_recipe(request.form):
        return redirect('/users/dashboard')
    return redirect('/recipes/create')

#read recipes
@app.route("/recipes/read_recipe/<int:id>")
def read_a_recipe(id):
    the_recipe = recipe.Recipe.get_recipe_by_id(id)
    return render_template("recipe.html", the_recipe=the_recipe)

#update recipes
@app.route("/recipes/edit/<int:id>")
def edit_a_recipe(id):
    the_recipe = recipe.Recipe.get_recipe_by_id(id)
    return render_template("edit.html", the_recipe=the_recipe)

@app.route("/recipes/updated", methods = ["POST"])
def updated_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    # the_recipe = recipe.Recipe.get_recipe_by_id(id)
    if recipe.Recipe.update_recipe_by_id(request.form) == True:
        print("&&&^&%$%&^&^&^&&&&& this is the request", request.form)
        return redirect("/users/dashboard")
    return render_template("edit.html", the_recipe=request.form)
    

    # if 'user_id' not in session:
    #     return redirect('/logout')
    # if not recipe.Recipe.validated_recipe(request.form):
    #     return render_template("edit.html", the_recipe=request.form)
    # data = {
    #     "name": request.form["name"],
    #     "description": request.form["description"],
    #     "instructions": request.form["instructions"],
    #     "under_thirty": int(request.form["under_thirty"]),
    #     "date_made": request.form["date_made"],
    #     "id": request.form['id']
    # }
    # recipe.Recipe.update_recipe_by_id(data)
    # return redirect("/users/dashboard")

#delete recipes
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    recipe.Recipe.delete_recipe_by_id(id)
    return redirect("/users/dashboard")