import math
from flask import (
    render_template, redirect, request, url_for, flash,
    session, Blueprint, current_app)
from bson.objectid import ObjectId
from app import mongo
from app.helpers import Helpers

recipes = Blueprint("recipes", __name__)

# Collections
coll_recipes = mongo.db.recipes
coll_users = mongo.db.users
coll_cuisines = mongo.db.cuisines
coll_courses = mongo.db.courses
coll_allergens = mongo.db.allergens


# Show All Recipes Page
@recipes.route("/show_recipes")
def show_recipes():
    """
    Render and display all recipes stored in the database. Reads
    page arguments to determine current page. Limits returned
    recipes to eight per page. Determines number or pages needed
    for pagination and passes to the template. Also sorts based on
    page arguments.
    """
    args = request.args.get

    # Read page arguments and set defaults if None.
    sort_type = args(str("sort")) or "views"
    page_args = int(args("page")) if args("page") is not None else 1
    order_type = int(args("order")) if args("order") else -1

    # Find all recipes and display based on arguments.
    sort = coll_recipes.find().skip((page_args * 8) - 8).limit(8).sort(
        [(sort_type, order_type)])

    # Pagination
    pages, previous_page, next_page, count, total_recipes, recipe_count = Helpers.pagination(
        sort, page_args, coll_recipes)

    return render_template(
        "showrecipes.html",
        recipes=sort,
        recipe_count=recipe_count,
        total_recipes=total_recipes,
        count=count,
        pages=pages,
        page=page_args,
        previous_page=previous_page,
        next_page=next_page)


# Add Recipe Page
@recipes.route("/add_recipe")
def add_recipe():
    """
    Renders the Add Recipe page, populates dropdowns and
    passes everything to the template.
    """
    cuisine, course, allergens = Helpers.dropdowns(coll_cuisines, coll_courses, coll_allergens)
    return render_template(
        "addrecipe.html",
        cuisine=sorted(cuisine),
        course=course,
        allergens=allergens)


# Add Recipe - Insert Recipe Function
@recipes.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    """
    Takes all values from the recipe form and builds a recipe
    JSON object. Method then inserts object into the database
    and redirects user to the Recipe Detail page for the new
    recipe.
    """

    author = coll_users.find_one({"username_lower": session["user"]})["_id"]
    # Split the ingredients and preparation steps into lists

    ingredients = request.form.get("ingredients").splitlines()
    prepSteps = request.form.get("prepSteps").splitlines()

    # Recipe JSON object
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
    coll_users.update_one(
        {"_id": ObjectId(author)},
        {"$push": {"user_recipes": insertRecipe.inserted_id}})
    flash("Thank you! Your recipe has been submitted!")
    return redirect(url_for(
        "recipes.recipe_detail",
        recipe_id=insertRecipe.inserted_id))


# Recipe Detail Page
@recipes.route("/recipe_detail/<recipe_id>")
def recipe_detail(recipe_id):
    """
    Renders the recipe detail page, pulls and returns the recipe
    info to the template. Also attempts to pull a list of the
    user's existing favourites and return them to the template
    to check if the recipe is an existing favourite. Method then
    increments the recipe 'views' field by 1.
    """
    recipe_name = coll_recipes.find_one({"_id": ObjectId(recipe_id)})
    author = coll_users.find_one(
        {"_id": ObjectId(recipe_name.get("author"))})["username"]
    user_img = coll_users.find_one(
        {"_id": ObjectId(recipe_name.get("author"))})["user_img"]

    # Attempt to retrieve user's favourites as a list
    try:
        favourite = coll_users.find_one(
            {"username_lower": session["user"]})["user_favs"]
    except:
        favourite = []

    coll_recipes.update(
        {"_id": ObjectId(recipe_id)}, {"$inc": {"views": 1}})
    return render_template(
        "recipedetail.html",
        image=user_img,
        recipe=recipe_name,
        author=author,
        favourites=favourite)


# Add Favourite Function
@recipes.route("/add_favourite/<recipe_id>")
def add_favourite(recipe_id):
    """
    Takes the current recipe ID and inserts it into the favourites
    field in their user record.
    """
    user = coll_users.find_one(
        {"username_lower": session["user"]})["_id"]
    coll_users.update_one(
        {"_id": ObjectId(user)},
        {"$push": {"user_favs": ObjectId(recipe_id)}})
    coll_recipes.update(
        {"_id": ObjectId(recipe_id)}, {"$inc": {"favourites": 1}})
    return redirect(url_for(
        "recipes.recipe_detail",
        recipe_id=recipe_id))


# Remove Favourite Function
@recipes.route("/remove_favourite/<recipe_id>")
def remove_favourite(recipe_id):
    """
    Takes the current recipe ID and removes it from the the user's
    favourites. Only available if the favourite exists.
    """
    user = coll_users.find_one({"username_lower": session["user"]})["_id"]
    coll_users.update_one(
        {"_id": ObjectId(user)},
        {"$pull": {"user_favs": ObjectId(recipe_id)}})
    coll_recipes.update(
        {"_id": ObjectId(recipe_id)}, {"$inc": {"favourites": -1}})
    return redirect(url_for(
        "recipes.recipe_detail",
        recipe_id=recipe_id))


# Update Recipe Page
@recipes.route("/update_recipe/<recipe_id>")
def update_recipe(recipe_id):
    """
    Renders the Update Recipe page and passes the selected
    recipe's details to the template to pre-populate all of
    the fields.
    """
    selected_recipe = coll_recipes.find_one({"_id": ObjectId(recipe_id)})
    steps = selected_recipe.get("prepSteps")
    cuisine, course, allergens = Helpers.dropdowns(coll_cuisines, coll_courses, coll_allergens)
    return render_template(
        "updaterecipe.html",
        selected_recipe=selected_recipe,
        cuisine=sorted(cuisine),
        course=course,
        allergens=allergens,
        steps=steps)


# Update Recipe - Insert Update Function
@recipes.route("/insert_update/<recipe_id>", methods=["POST"])
def insert_update(recipe_id):
    """
    Takes all values from the recipe form and builds a recipe
    JSON object. Method then inserts object into the database,
    overwriting the original, and redirects back to the Recipe
    Detail page.
    """
    if request.method == "POST":
        recipe = coll_recipes.find_one({"_id": ObjectId(recipe_id)})
        ingredients = request.form.get("ingredients").splitlines()
        prepSteps = request.form.get("prepSteps").splitlines()
        author = recipe.get("author")
        currentViews = recipe.get("views")
        currentFavs = recipe.get("favourites")
        coll_recipes.update({"_id": ObjectId(recipe_id)}, {
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
        flash(f"Thank you! Your update has been submitted!")
        return redirect(url_for(
            "recipes.recipe_detail",
            recipe_id=recipe_id))


# Delete Recipe Function
@recipes.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """
    Deletes the selected recipe, removes it from the user's
    favourites, and redirects to display all recipes.
    """
    user = coll_users.find_one({"username_lower": session["user"]})["_id"]
    coll_recipes.remove({"_id": ObjectId(recipe_id)})
    coll_users.update_one(
        {"_id": ObjectId(user)},
        {"$pull": {"user_recipes": ObjectId(recipe_id)}})
    return redirect(url_for("recipes.show_recipes"))


# Search Page
@recipes.route("/search_recipes")
def search_recipes():
    """
    Method searches through the database based on user choices from entered
    keywords, and dropdowns. Returns the results to the template with info
    on how many results were returned.
    """
    cuisine, course, allergens = Helpers.dropdowns(coll_cuisines, coll_courses, coll_allergens)
    args = request.args.get
    args_list = request.args.getlist

    # Get Search and Pagination arguments from URL
    keyword_args = (
        args("search_keys") if args("search_keys") is not None else "")
    cuisineFilter_args = (
        args("cuisine_filter") if args("cuisine_filter") is not None else "")
    courseFilter_args = (
        args("course_filter") if args("course_filter") is not None else "")
    allergenFilter_args = (
        args_list("allergen_filter") if args_list(
            "allergen_filter") is not None else [])
    page_args = int(args("page")) if args("page") is not None else 1

    # Set search variables
    search_keywords = (
        keyword_args.split() if keyword_args is not None else "")
    search_cuisine = (
        cuisineFilter_args if cuisineFilter_args is not None else "")
    search_course = (
        courseFilter_args if courseFilter_args is not None else "")
    search_allergens = (
        allergenFilter_args if allergenFilter_args != [] else "")

    # Join search variables and perform search
    search = (
        '"' + '" "'.join(search_keywords) +
        '" "' + ''.join(search_cuisine) +
        '" "' + ''.join(search_course) +
        '"' + ' -' + ' -'.join(search_allergens))
    search_results = coll_recipes.find(
        {"$text": {"$search": search}}).skip((page_args * 8) - 8)\
        .limit(8).sort([("views", -1)])

    # Pagination
    (
        pages, previous_page, next_page, count,
        total_recipes, results_count) = Helpers.pagination(
        search_results, page_args, coll_recipes)

    return render_template(
        "searchrecipes.html",
        recipes=search_results,
        cuisine=sorted(cuisine),
        course=course,
        allergens=allergens,
        keywords=keyword_args,
        f_cuisine=cuisineFilter_args,
        f_course=courseFilter_args,
        f_allergen=allergenFilter_args,
        pages=pages,
        results_count=results_count,
        total_recipes=total_recipes,
        count=count,
        page=page_args,
        next_page=next_page,
        previous_page=previous_page)
