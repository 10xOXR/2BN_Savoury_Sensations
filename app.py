import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "m4recipesCollection"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

mongo = PyMongo(app)

# Collections

coll_users = mongo.db.users
coll_recipes = mongo.db.recipes
coll_cuisines = mongo.db.cuisines
coll_courses = mongo.db.courses
coll_allergens = mongo.db.allergens

# Helper functions

def dropdowns(list1, list2, list3):
        for types in coll_cuisines.find():
                cuisine_type = types.get("cuisineType")
                for item in cuisine_type:
                        list1.append(item)
        for types in coll_courses.find():
                course_type = types.get("courseType")
                for item in course_type:
                        list2.append(item)
        for types in coll_allergens.find():
                allergen_type = types.get("allergenType")
                for item in allergen_type:
                        list3.append(item)

# Routes

@app.route("/")
@app.route("/show_recipes")
def show_recipes():
        alpha_sort = coll_recipes.find().sort( [("views", -1)] )
        total_recipes = coll_recipes.count()
        return render_template("showrecipes.html", recipes = alpha_sort, total_recipes = total_recipes)

@app.route("/add_recipe")
def add_recipe():
        cuisine = []
        course = []
        allergens = []
        dropdowns(cuisine, course, allergens)
        return render_template("addrecipe.html", cuisine = sorted(cuisine), course = course, allergens = allergens)

@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
        ingredients = request.form.get('ingredients').splitlines()
        prepSteps = request.form.get('prepSteps').splitlines()
        submission = {
                "cuisineType": request.form.get('cuisineType'),
                "courseType": request.form.get('courseType'),
                "recipeName": request.form.get('recipe_name'),
                "recipeDesc": request.form.get('recipeDesc'),
                "ingredients": ingredients,
                "prepSteps": prepSteps,
                "prepTime": request.form.get('prepTime'),
                "cookTime": request.form.get('cookTime'),
                "temp": request.form.get('temp'),
                "allergens": request.form.getlist('allergens'),
                "imgUrl": request.form.get('imageUrl'),
                "views": 0
        }
        insertRecipe = coll_recipes.insert_one(submission)
        flash('Thank you! Your recipe has been submitted!')
        return redirect(url_for("recipe_detail", recipe_id = insertRecipe.inserted_id))

@app.route("/recipe_detail/<recipe_id>")
def recipe_detail(recipe_id):
        recipe_name = coll_recipes.find_one({"_id": ObjectId(recipe_id)})
        coll_recipes.update({"_id": ObjectId(recipe_id)}, {'$inc': {'views': 1}})
        return render_template("recipedetail.html", recipe = recipe_name)

@app.route("/update_recipe/<recipe_id>")
def update_recipe(recipe_id):
        cuisine = []
        course = []
        allergens = []
        selected_recipe = coll_recipes.find_one({"_id": ObjectId(recipe_id)})
        steps = selected_recipe.get("prepSteps")
        dropdowns(cuisine, course, allergens)
        return render_template("updaterecipe.html", selected_recipe = selected_recipe, cuisine = sorted(cuisine), 
                                course = course, allergens = allergens, steps = steps)

@app.route("/insert_update/<recipe_id>", methods=["POST"])
def insert_update(recipe_id):
        recipe = coll_recipes.find_one({"_id": ObjectId(recipe_id)})
        ingredients = request.form.get('ingredients').splitlines()
        prepSteps = request.form.get('prepSteps').splitlines()
        currentViews = recipe.get("views")
        coll_recipes.update({"_id": ObjectId(recipe_id)}, {
                "cuisineType": request.form.get('cuisineType'),
                "courseType": request.form.get('courseType'),
                "recipeName": request.form.get('recipe_name'),
                "recipeDesc": request.form.get('recipeDesc'),
                "ingredients": ingredients,
                "prepSteps": prepSteps,
                "prepTime": request.form.get('prepTime'),
                "cookTime": request.form.get('cookTime'),
                "temp": request.form.get('temp'),
                "allergens": request.form.getlist('allergens'),
                "imgUrl": request.form.get('imageUrl'),
                "views": currentViews
        })
        flash('Thank you! Your update has been submitted!')
        return redirect(url_for("recipe_detail", recipe_id = recipe_id))

@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
        coll_recipes.remove({"_id": ObjectId(recipe_id)})
        return redirect(url_for("show_recipes"))

@app.route("/search")
def search():
        cuisine = []
        course = []
        allergens = []
        dropdowns(cuisine, course, allergens)
        return render_template("searchrecipes.html", cuisine = sorted(cuisine), course = course, 
                                allergens = allergens)

@app.route("/search_recipes", methods=["POST"])
def search_recipes():
        cuisine = []
        course = []
        allergens = []
        keywords = request.form.get("search_keys").split()
        cuisineFilter = ""
        courseFilter = ""
        allergenFilter = ""

        dropdowns(cuisine, course, allergens)

        if request.form.get("cuisineFilter") == None:
                cuisineFilter = ""
        else:
                cuisineFilter = request.form.get("cuisineFilter").split()
        
        if request.form.get("courseFilter") == None:
                courseFilter = ""
        else:
                courseFilter = request.form.get("courseFilter").split()
        
        if request.form.get("allergenFilter") == None:
                allergenFilter = ""
        else:
                allergenFilter = request.form.getlist("allergenFilter")

        search = '"' + '" "'.join(keywords) + '" "' + ''.join(cuisineFilter) + '" "' + ''.join(courseFilter) + '"' + ' -' + ' -'.join(allergenFilter)
        print(search)
        search_results = coll_recipes.find({"$text": {"$search": search}}).sort( [("views", -1)])

        return render_template("searchrecipes.html", recipes = search_results, cuisine = sorted(cuisine), course = course, 
                                allergens = allergens, f_cuisine = request.form.get("cuisineFilter"),
                                f_course = request.form.get("courseFilter"), f_allergen = allergenFilter)

if __name__ == "__main__":
        app.run(host=os.environ.get("IP"),
        port=os.environ.get("PORT"),
        debug=True)