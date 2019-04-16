import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "m4RecipiesCollection"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Collections
coll_users = mongo.db.users
coll_recipies = mongo.db.recipes
coll_cuisine = mongo.db.cuisine

@app.route("/")
@app.route("/show_recipes")
def show_recipes():
        alpha_sort = coll_recipies.find().sort( [("recipeName", 1)] )
        total_recipes = coll_recipies.count()
        return render_template("showrecipes.html", recipes = alpha_sort, total_recipes = total_recipes)

@app.route("/add_recipe")
def add_recipe():
        cuisine = []
        course = []
        allergens = []
        for types in coll_cuisine.find():
                cuisine_type = types.get('cuisineType')
                course_type = types.get('courseType')
                allergen_type = types.get('allergens')
                for item in cuisine_type:
                        cuisine.append(item)
                for item in course_type:
                        course.append(item)
                for item in allergen_type:
                        allergens.append(item)
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
                "imgUrl": request.form.get('imageUrl')
        }
        coll_recipies.insert_one(submission)
        flash('Thank you! Your recipe has been submitted!')
        return redirect(url_for("add_recipe"))

@app.route("/recipe_detail/<recipe_id>")
def recipe_detail(recipe_id):
        recipe_name = coll_recipies.find_one({"_id": ObjectId(recipe_id)})
        coll_recipies.update({"_id": ObjectId(recipe_id)}, {'$inc': {'views': 1}})
        return render_template("recipedetail.html", recipe = recipe_name)

if __name__ == "__main__":
        app.run(host=os.environ.get("IP"),
        port=os.environ.get("PORT"),
        debug=True)