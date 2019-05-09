#!/usr/bin/env python3
import os
import random
import math
from flask import Flask, render_template, redirect, request, url_for, flash, Markup, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

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

# Landing Page
@app.route("/home")
def landing_page():
        slideshow = [recipe for recipe in coll_recipes.aggregate([{"$sample": {"size": 5}}])]
        return render_template("landing.html", slideshow = slideshow)

# User Sign-up Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
        if request.method == "POST":
                registered_user = coll_users.find_one({"username_lower": request.form.get("username").lower()})
                if registered_user:
                        flash(f"Sorry, but {request.form.get('username')} has already been taken.")
                        return render_template("signup.html")

                if len(request.form.get("username")) < 5 or len(request.form.get("username")) > 15:
                        flash("Usernames should be 5 - 15 characters long.")
                        return render_template("signup.html")

                if len(request.form.get("password")) < 5 or len(request.form.get("password")) > 15:
                        flash("Passwords should be 5 - 15 characters long.")
                        return render_template("signup.html")

                if request.form.get("password") != request.form.get("password-check"):
                        flash("Supplied passwords do not match.")
                        return render_template("signup.html")

                # Generates a profile picture based on entered username, inserting randomised URL choices
                shapes = ["squares/", "isogrids/", "spaceinvaders/", "labs/isogrids/hexa/", "labs/isogrids/hexa16/"]
                theme = ["frogideas", "sugarsweets", "heatwave", "daisygarden", "seascape", "summerwarmth", "duskfalling", "berrypie"]
                user_image = "https://www.tinygraphs.com/" + random.choice(shapes) + request.form.get("username") + "?theme=" + random.choice(theme) + "&numcolors=4&size=220&fmt=svg"
                
                user = {
                        "username": request.form.get("username"),
                        "username_lower": request.form.get("username").lower(),
                        "password": generate_password_hash(request.form.get("password")),
                        "user_img": user_image,
                        "user_recipes": [],
                        "user_favs": []
                }
                coll_users.insert_one(user)
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("profile", username = session["user"]))

        return render_template("signup.html")

#User Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
        if request.method == "POST":
                registered_user = coll_users.find_one({"username_lower": request.form.get("username").lower()})
                if registered_user:
                        if check_password_hash(registered_user["password"], request.form.get("password")):
                                session["user"] = request.form.get("username").lower()
                                return redirect(url_for("profile", username = session["user"]))
                        else:
                                flash("Incorrect Username or Password")
                                return render_template("login.html")
                else:
                        flash("Incorrect Username or Password")
                        return render_template("login.html")

        return render_template("login.html")

#User Profile Page
@app.route("/profile/<username>")
def profile(username):
        user_img = coll_users.find_one({"username_lower": username})["user_img"]
        user = coll_users.find_one({"username_lower": username})["username"]
        favs = coll_users.find_one({"username_lower": username})["user_favs"]
        own_recipes = coll_users.find_one({"username_lower": username})["user_recipes"]
        fav_rec = coll_recipes.find({"_id": {"$in": favs}}).sort( [("views", -1)] )
        own_rec = coll_recipes.find({"_id": {"$in": own_recipes}}).sort( [("views", -1)] )
        return render_template("profile.html", image = user_img, username = user, favs = fav_rec, own_rec = own_rec)

# Change Password
@app.route("/change-password/<username>", methods=["GET", "POST"])
def change_password(username):
        if request.method == "POST":
                if check_password_hash(coll_users.find_one({"username_lower": username})["password"], request.form.get("old-password")):
                        if len(request.form.get("new-password")) < 5 or len(request.form.get("new-password")) > 15:
                                flash("Passwords should be 5 - 15 characters long.")
                                return redirect(url_for("change_password", username = session["user"]))
                        if request.form.get("new-password") == request.form.get("password-check"):
                                coll_users.update_one({"username_lower": username}, {"$set": {"password": generate_password_hash(request.form.get("new-password"))}})
                        else:
                                flash("New passwords do not match!")
                                return redirect(url_for("change_password", username = session["user"]))
                else:
                        flash("Original password is incorrect!")
                        return redirect(url_for("change_password", username = session["user"]))
                flash("Your password was updated successfully!")
                return redirect(url_for("profile", username = session["user"]))

        return render_template("changepassword.html", username = session["user"])

# User Logout
@app.route("/logout")
def logout():
        session.pop("user")
        return redirect(url_for("landing_page"))


# Show All Recipes Page
@app.route("/")
@app.route("/show_recipes/skip:<skip>")
def show_recipes(skip = 0):

        sort_type = request.args.get(str("sort")) or "views"
        order_type = int(request.args.get("order")) if request.args.get("order") else -1
        sort = coll_recipes.find().skip(int(skip)).limit(8).sort( [(sort_type, order_type)] )
        page_count = range(0, math.ceil(sort.count() / 8))
        skips = [page * 8 for page in page_count]

        count = int(skip) + 8 if (int(skip) + 8) < sort.count() else sort.count()
        total_recipes = coll_recipes.count()
        
        return render_template("showrecipes.html", recipes = sort, total_recipes = total_recipes, count = count, skip = int(skip),
                                skips = skips)

# Add Recipe Page
@app.route("/add_recipe")
def add_recipe():
        cuisine = []
        course = []
        allergens = []
        dropdowns(cuisine, course, allergens)
        return render_template("addrecipe.html", cuisine = sorted(cuisine), course = course, allergens = allergens)

# Add Recipe - Insert Recipe Function
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
        author = coll_users.find_one({"username_lower": session["user"]})["_id"]
        ingredients = request.form.get("ingredients").splitlines()
        prepSteps = request.form.get("prepSteps").splitlines()
        submission = {
                "cuisineType": request.form.get("cuisineType"),
                "courseType": request.form.get("courseType"),
                "recipeName": request.form.get("recipe_name"),
                "recipeDesc": request.form.get("recipeDesc"),
                "ingredients": ingredients,
                "prepSteps": prepSteps,
                "prepTime": request.form.get("prepTime"),
                "cookTime": request.form.get("cookTime"),
                "temp": request.form.get("temp"),
                "allergens": request.form.getlist("allergens"),
                "imgUrl": request.form.get("imageUrl"),
                "author": author,
                "views": 0,
                "favourites": 0
        }
        insertRecipe = coll_recipes.insert_one(submission)
        coll_users.update_one({"_id": ObjectId(author)}, {"$push": {"user_recipes": insertRecipe.inserted_id}})
        flash("Thank you! Your recipe has been submitted!")
        return redirect(url_for("recipe_detail", recipe_id = insertRecipe.inserted_id))

# Recipe Detail Page
@app.route("/recipe_detail/<recipe_id>")
def recipe_detail(recipe_id):
        recipe_name = coll_recipes.find_one({"_id": ObjectId(recipe_id)})
        author = coll_users.find_one({"_id": ObjectId(recipe_name.get("author"))})["username"]

        try:
                favourite = coll_users.find_one({"username_lower": session["user"]})["user_favs"]
        except:
                favourite = []
                
        coll_recipes.update({"_id": ObjectId(recipe_id)}, {"$inc": {"views": 1}})
        return render_template("recipedetail.html", recipe = recipe_name, author = author, favourites = favourite)

# Add Favourite Function
@app.route("/add_favourite/<recipe_id>")
def add_favourite(recipe_id):
        user = coll_users.find_one({"username_lower": session["user"]})["_id"]
        coll_users.update_one({"_id": ObjectId(user)}, {"$push": {"user_favs": ObjectId(recipe_id)}})
        coll_recipes.update({"_id": ObjectId(recipe_id)}, {"$inc": {"favourites": 1}})
        return redirect(url_for("recipe_detail", recipe_id = recipe_id))

# Update Recipe Page
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

# Update Recipe - Insert Update Function
@app.route("/insert_update/<recipe_id>", methods=["POST"])
def insert_update(recipe_id):
        recipe = coll_recipes.find_one({"_id": ObjectId(recipe_id)})
        ingredients = request.form.get("ingredients").splitlines()
        prepSteps = request.form.get("prepSteps").splitlines()
        author = recipe.get("author")
        currentViews = recipe.get("views")
        currentFavs = recipe.get("favourites")
        coll_recipes.update_one({"_id": ObjectId(recipe_id)}, {
                "cuisineType": request.form.get("cuisineType"),
                "courseType": request.form.get("courseType"),
                "recipeName": request.form.get("recipe_name"),
                "recipeDesc": request.form.get("recipeDesc"),
                "ingredients": ingredients,
                "prepSteps": prepSteps,
                "prepTime": request.form.get("prepTime"),
                "cookTime": request.form.get("cookTime"),
                "temp": request.form.get("temp"),
                "allergens": request.form.getlist("allergens"),
                "imgUrl": request.form.get("imageUrl"),
                "author": author,
                "views": currentViews,
                "favourites": currentFavs
        })
        flash("Thank you! Your update has been submitted!")
        return redirect(url_for("recipe_detail", recipe_id = recipe_id))

# Delete Recipe Function
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
        user = coll_users.find_one({"username_lower": session["user"]})["_id"]
        coll_recipes.remove({"_id": ObjectId(recipe_id)})
        coll_users.update_one({"_id": ObjectId(user)}, {"$pull": {"user_recipes": ObjectId(recipe_id)}})
        return redirect(url_for("show_recipes"))

# Search Page
@app.route("/search_recipes/skip:<skip>", methods=["GET", "POST"])
def search_recipes(skip = 0):
        cuisine = []
        course = []
        allergens = []
        dropdowns(cuisine, course, allergens)

        keywords = request.form.get("search_keys").split() if request.form.get("search_keys") != None else ""
        cuisineFilter = request.form.get("cuisineFilter") if request.form.get("cuisineFilter") != None else "" 
        courseFilter = courseFilter = request.form.get("courseFilter") if request.form.get("courseFilter") != None else ""
        allergenFilter = request.form.getlist("allergenFilter") if request.form.get("allergenFilter") != None else ""
        
        search = '"' + '" "'.join(keywords) + '" "' + ''.join(cuisineFilter) + '" "' + ''.join(courseFilter) + '"' + ' -' + ' -'.join(allergenFilter)
        search_results = coll_recipes.find({"$text": {"$search": search}}).skip(int(skip)).limit(8).sort( [("views", -1)])
        # Pagination
        page_count = range(0, math.ceil(search_results.count() / 8))
        skips = [page * 8 for page in page_count]
        count = int(skip) + 8 if (int(skip) + 8) < search_results.count() else search_results.count()

        return render_template("searchrecipes.html", recipes = search_results, cuisine = sorted(cuisine), course = course, 
                                allergens = allergens, f_cuisine = request.form.get("cuisineFilter"),
                                f_course = request.form.get("courseFilter"), f_allergen = allergenFilter, skips = skips,
                                results_count = search_results.count(), count = count, skip = int(skip))

if __name__ == "__main__":
        app.run(host=os.environ.get("IP"),
        port=os.environ.get("PORT"),
        debug=True)