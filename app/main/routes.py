from flask import render_template, Blueprint, current_app
from app import mongo

main = Blueprint("main", __name__)

# Collections
coll_recipes = mongo.db.recipes


# Landing Page
@main.route("/")
@main.route("/home")
def landing_page():
    """
    Render the landing/homepage and populates the Materialize
    carousel with random recipes.
    """
    # Select 5 random recipes from the database to use in the
    # homepage carousel
    slideshow = [recipe for recipe in coll_recipes.aggregate(
            [{"$sample": {"size": 5}}])]
    return render_template("landing.html", slideshow=slideshow)
