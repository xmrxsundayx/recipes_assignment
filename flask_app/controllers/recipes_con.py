from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import users_mod
from flask_app.models import recipe_mod
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

    # *****RECIPE WALL*****

@app.route('/home')
def home():
    if 'id' not in session:
        return redirect('/logout')
    user_id = session['id']
    return redirect("/recipe/wall")

@app.route('/recipe/wall')
def to_the_wall():
    if 'id' not in session:
        return redirect('/logout')
    user_id = session['id']
    return redirect(f"/recipe/wall/{user_id}")
    
@app.route('/recipe/wall/<int:id>')
def welcome(id):
    if 'id' not in session:
        return redirect('/logout')
    user_in_DB = users_mod.Users.get_user_by_id({'id':id})
    if not user_in_DB:
        flash('Invalid User ID', 'login')
        return redirect('/')
    all_recipes = recipe_mod.Recipes.get_all()
    return render_template('recipe_wall.html',user_in_DB= user_in_DB, all_recipes=all_recipes)

# *****RECIPE ACTIONS*****

# *****VIEW*****

@app.route('/recipe/view/<int:id>')
def let_me_see(id):
    data = {
        'id': id
    }
    user_data = {
        'id': session['id']
    }
    recipe = recipe_mod.Recipes.get_by_id(data)
    one_user = users_mod.Users.get_user_by_id(user_data)
    return render_template('view_recipe.html',recipe = recipe, one_user= one_user)


# *****ADD*****

@app.route('/recipe/add')
def make_me():
    if 'id' not in session:
        return redirect('/logout')
    user_id = session['id']
    return render_template("add_recipes.html", user_id=user_id)


@app.route('/recipe/create',methods=['POST'])
def create_recipe():
    if not recipe_mod.Recipes.verify_recipe(request.form):
        return redirect('/recipe/add')
    recipe_data ={
        'user_id': request.form['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'under': request.form['under'],
    }
    one_recipe = recipe_mod.Recipes.save(recipe_data)
    return redirect('/recipe/wall')

# *****EDIT*****

@app.route('/recipe/edit/<int:id>')
def change_me(id):
    if 'id' not in session:
        return redirect('/logout')
    data={
        'id':id
    }
    return render_template("recipes_edit.html",recipe = recipe_mod.Recipes.get_recipe(data))

@app.route('/recipe/new_edit/<int:recipe_id>',methods=['POST'])
def edit_recipe(recipe_id):
    if not recipe_mod.Recipes.verify_recipe(request.form):
        return redirect(f'/recipe/edit/{recipe_id}')
    recipe_mod.Recipes.edit(request.form)
    return redirect('/recipe/wall')



# *****DELETE*****
@app.route('/recipe/delete/<recipe_id>')
def delete_post(recipe_id):
    print ('Deleting recipe - ', recipe_id)
    recipe_mod.Recipes.delete(recipe_id)
    return redirect('/recipe/wall')