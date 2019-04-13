import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "m4RecipiesCollection"
app.config["MONGO_URI"] = os.environ.get("MONGO_SECRET")

mongo = PyMongo(app)

# Collections
coll_users = mongo.db.users
coll_recipies = mongo.db.recipes
coll_cuisine = mongo.db.cuisine

@app.route("/")
@app.route("/add_recipe")
def add_recipe():
        cuisine = []
        course = []
        for types in coll_cuisine.find():
                cuisine_type = types.get('cuisineType')
                course_type = types.get('courseType')
                for item in cuisine_type:
                        cuisine.append(item)
                for item in course_type:
                        course.append(item)

        return render_template("addrecipe.html", cuisine = cuisine, course = course)

@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
        coll_recipies.insert_one(request.form.to_dict())
        return redirect(url_for("add_recipe"))

if __name__ == "__main__":
        app.run(host=os.environ.get("IP"),
        port=os.environ.get("PORT"),
        debug=True)