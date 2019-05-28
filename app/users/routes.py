import random
from flask import render_template, redirect, request, url_for, flash, session, Blueprint, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from app import mongo

users = Blueprint("users", __name__)

# Collections
coll_recipes = mongo.db.recipes
coll_users = mongo.db.users

# User Sign-up Page
@users.route("/signup", methods=["GET", "POST"])
def signup():
	"""
	Renders the signup page for users to create their account.
	Performs validation on the inputs to endure that they meet
	the requirements for the site, and then posts the details
	to the database. Generates browser session for user and 
	redirects to their profile page.
	"""
	if request.method == "POST":
		registered_user = coll_users.find_one({"username_lower": request.form.get("username").lower()})

		# Check that username hasn't already been registered.
		if registered_user:
			flash(f"Sorry, but {request.form.get('username')} has already been taken.")
			return render_template("signup.html")

		# Check length of usernames and flash error if outside limits
		if len(request.form.get("username")) < 5 or len(request.form.get("username")) > 15:
			flash("Usernames should be 5 - 15 characters long.")
			return render_template("signup.html")

		# Check length of passwords and flash error if outside limits
		if len(request.form.get("password")) < 5 or len(request.form.get("password")) > 15:
			flash("Passwords should be 5 - 15 characters long.")
			return render_template("signup.html")

		# Check that the supplied passwords match
		if request.form.get("password") != request.form.get("password-check"):
			flash("Supplied passwords do not match.")
			return render_template("signup.html")

		# Generates a profile picture based on entered username, inserting randomised URL choices
		shapes = ["squares/", "isogrids/", "spaceinvaders/", "labs/isogrids/hexa/", "labs/isogrids/hexa16/"]
		theme = ["frogideas", "sugarsweets", "heatwave", "daisygarden", "seascape", "summerwarmth", "duskfalling", "berrypie"]
		user_image = "https://www.tinygraphs.com/" + random.choice(shapes) + request.form.get("username") + "?theme=" + random.choice(theme) + "&numcolors=4&size=220&fmt=svg"
		
		# Populates JSON object with form data and user image
		user = {
			"username": request.form.get("username"),
			"username_lower": request.form.get("username").lower(),
			"password": generate_password_hash(request.form.get("password")),
			"user_img": user_image,
			"user_recipes": [],
			"user_favs": []
		}

		# Insert the user details into the database
		coll_users.insert_one(user)

		# Create browser session for new user and redirect to their profile page
		session["user"] = request.form.get("username").lower()
		return redirect(url_for("users.profile", username = session["user"]))

	return render_template("signup.html")

#User Login Page
@users.route("/login", methods=["GET", "POST"])
def login():
	"""
	Renders the login page and validates the infomation provided
	against the database user information. If valid, a session
	is created for the user and they are redirected to their
	profile page. Otherwise returns to login page displaying
	an error.
	"""
	if request.method == "POST":
		registered_user = coll_users.find_one({"username_lower": request.form.get("username").lower()})

		# Check that the user exists, and that the username and password match database
		if registered_user:
			if check_password_hash(registered_user["password"], request.form.get("password")):
				session["user"] = request.form.get("username").lower()
				return redirect(url_for("users.profile", username = session["user"]))
			else:
				flash("Incorrect Username or Password")
				return render_template("login.html")
		else:
			flash("Incorrect Username or Password")
			return render_template("login.html")

	return render_template("login.html")

#User Profile Page
@users.route("/profile/<username>")
def profile(username):
	"""
	Renders the user profile page, displaying their image, and
	both their own and favourite recipes. 
	"""
	# Gets the user information from the database
	user_img = coll_users.find_one({"username_lower": username})["user_img"]
	user = coll_users.find_one({"username_lower": username})["username"]
	favs = coll_users.find_one({"username_lower": username})["user_favs"]
	own_recipes = coll_users.find_one({"username_lower": username})["user_recipes"]

	# Searches database for the recipe information stored in user profile
	fav_rec = coll_recipes.find({"_id": {"$in": favs}}).sort( [("views", -1)] )
	own_rec = coll_recipes.find({"_id": {"$in": own_recipes}}).sort( [("views", -1)] )
	
	return render_template(
		"profile.html",
		image = user_img,
		username = user,
		favs = fav_rec,
		own_rec = own_rec)

# Change Password
@users.route("/change-password/<username>", methods=["GET", "POST"])
def change_password(username):
	"""
	Renders page allowing users to change their password. Checks
	current password against database and then validates the new
	password meets requirements and both new fields match. Inserts
	new password to user profile in database and redirects to the
	profie page.
	"""
	if request.method == "POST":
		if check_password_hash(coll_users.find_one({"username_lower": username})["password"], request.form.get("old-password")):
			# Check length of passwords and flash error if outside limits
			if len(request.form.get("new-password")) < 5 or len(request.form.get("new-password")) > 15:
				flash("Passwords should be 5 - 15 characters long.")
				return redirect(url_for("users.change_password", username = session["user"]))

				# Check new passwords match and updates profile with new password
			if request.form.get("new-password") == request.form.get("password-check"):
				coll_users.update_one({"username_lower": username}, {"$set": {"password": generate_password_hash(request.form.get("new-password"))}})
			else:
				flash("New passwords do not match!")
				return redirect(url_for("users.change_password", username = session["user"]))
		else:
			flash("Original password is incorrect!")
			return redirect(url_for("users.change_password", username = session["user"]))
		# Redirect to user profile page, flashing success message
		flash("Your password was updated successfully!")
		return redirect(url_for("users.profile", username = session["user"]))

	return render_template("changepassword.html", username = session["user"])

# Delete Account
@users.route("/delete-account/<username>", methods=["POST"])
def delete_account(username):
	"""
	Method to delete the current user's profile, with the option
	to remove all of their recipes from the database. If not
	deleted, all user's recipes are reassigned to the Admin
	account. 'Favourites' interger is decremented by one for 
	each recipe user has in their favourites. Session is then
	terminated and redirects to homepage.
	"""
	user = coll_users.find_one({"username_lower": username})
	if check_password_hash(user["password"], request.form.get("password")):
		user_rec = [recipe for recipe in user.get("user_recipes")]

		# If checkbox selected, deletes all user recipes and remove from other
		# users' favourite recipes.
		if request.form.get("del-recipes") == "on":
			for item in user_rec:
				coll_recipes.remove({"_id": item})
				coll_users.update_many({}, {"$pull": {"user_favs": item}})

		# If user chooses not to delete their recipes, reassign the author to Admin
		admin = coll_users.find_one({"username_lower": "admin"})["_id"]
		for item in user_rec:
			coll_recipes.update({"_id": item}, {"$set": {"author": admin}})
			coll_users.update({"_id": admin}, {"$push": {"user_recipes": item}})

		# Decrement all recipes' "favourite" integers that user had in their own favourites
		user_favs = [fav for fav in user.get("user_favs")]
		for fav in user_favs:
			coll_recipes.update({"_id": fav}, {"$inc": {"favourites": -1}})

		# Delete User session
		session.pop("user")

		# Delete user record
		coll_users.remove({"_id": user.get("_id")})
		return redirect(url_for("main.landing_page"))
	else:
		flash("Incorrect Password")
		return redirect(request.referrer)

# User Logout
@users.route("/logout")
def logout():
	""" Logs user out and redirects to homepage """
	session.pop("user")
	return redirect(url_for("main.landing_page"))
