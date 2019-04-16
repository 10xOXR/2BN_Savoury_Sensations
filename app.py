import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "m4RecipiesCollection"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Collections
coll_users = mongo.db.users
coll_recipies = mongo.db.recipes
coll_cuisine = mongo.db.cuisine

@app.route("/")
@app.route("/show_recipes")
def show_recipes():
        return render_template("showrecipes.html", recipes = coll_recipies.find())

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

if __name__ == "__main__":
        app.run(host=os.environ.get("IP"),
        port=os.environ.get("PORT"),
        debug=True)