# [2BN Savoury Sensations](https://https://m4-2bn-savoury-sensations.herokuapp.com)

<img src="https://github.com/10xOXR/2BN_Savoury_Sensations/blob/master/design/mockups.png" alt="2BN-Savoury-Sensations" width="800">


We all need food, so why not make the experience something wonderful; something worth remembering? 2BN Savoury Sensations was created to help serve that purpose by bringing together the tastiest savoury recipes from around the world! 

---

## Table of Contents
1. [**UX**](#ux)
    - [**User Stories**](#user-stories)
    - [**Design**](#design)
        - [**Framework**](#framework)
        - [**Color Scheme**](#color-scheme)
        - [**Typography**](#typography)
    - [**Wireframes**](#wireframes)

2. [**Features**](#features)
    - [**Existing Features**](#existing-features)
    - [**Features Left to Implement**](#features-left-to-implement)

3. [**Technologies Used**](#technologies-used)

4. [**Testing**](#testing)
    - [**Testing**](#testing)
    - [**Validators**](#validators)
    - [**Compatibility**](#compatibility)

5. [**Deployment**](#deployment)
    - [**Local Deployment**](#local-deployment)
    - [**Remote Deployment**](#remote-deployment)

6. [**Credits**](#credits)
    - [**Content**](#content)
    - [**Media**](#media)
    - [**Code**](#code)
    - [**Acknowledgements**](#acknowledgements)

---

## UX

As fantastic as this sounds, this also serves as my Data-Centric Milestone project for [Code Institute](https://codeinstitute.net/), as part of the Full-Stack Software Development course. The brief for this project requires the creation of an online recipe book which allows users to **C**reate, **R**ead, **U**pdate, and **D**elete their own recipes, and to browse/save the recipes created by others. 

### User Stories

Users of the site should be able to:

- access the site using their preferred device (mobile, tablet, desktop) without any loss of functionality.
 - browse all recipes and view recipe details as a guest without the need to create an account.
 - sort the displayed recipes based on the number of views the recipe has, the number of users that have saved it to their favourites, or alphabetically.
 - register a user account and have their chosen password be stored in the database only as a 256-bit salted hash and not in plain text.
 - view a profile area that displays all of the recipes that they have created, as well as any recipes that they have added to their favourites.
 - add and remove recipes from their saved favourites.
 - change their existing password.
 - delete their account with the option to also delete all of the recipes that they have created.
 - have all of their recipes re-assigned to the Admin account should they choose not to delete them when removing their user account.
 - log out of their account and have the session terminated.
- add recipes to the site along with the URL of a picture that best represents their creation, or have a placeholder picture if they are unable to provide a URL.
- edit any recipe that they have created in line with the requirements of the site.
- delete any of their recipes, and have those recipes removed from the favourites of all other users that may have saved it.
- view the details of any recipe, including all ingredients, preparation instructions, allergens, and the time required to cook the meal.
- search the recipe database based on keywords, cuisine type, course type, and filter out potential allergens.


### Design

The design of the site is based on standard Materialize elements, with their colouring altered to give the site a pleasing, neutral tone. Recipes are displayed on site as Cards, which display the recipe image, name, and details of how many views and favourites that each recipe has. A single food-related background image is used on all pages on the site. 

#### Framework

Frameworks used in the project are:

 - [Materialize 1.0.0](https://materializecss.com/)
    - Using the Materialize framework allowed for the development of a clean and modern user interface with minimal need to override or alter the default settings in most cases.
- [Flask 1.0.2](https://www.djangoproject.com/)
    - Flask is used as the templating micro-framework that renders all pages on the site.
- [jQuery 3.3.1](https://code.jquery.com/jquery/)
    - Although mostly unbound from jQuery in version 1.0.0, Materialize still requires some jQuery in order to properly initialize its elements (such as dropdowns, carousels, etc.). It is also used for custom functions, including  as part of custom recipe sorting.

#### Color Scheme

Colours on te site are all based around a single colour, ![#0E5F76](https://placehold.it/15/0E5F76/0E5F76) `#0E5F76` , as I found that this was the most visually pleasing way of bringing together all of the visual elements on the site. 

#### Typography

All fonts used on the site are those provided by the Materialize framework. No custom fonts were used as I felt that they detracted from the content.

### Wireframes

[Balsamiq Wireframes](https://balsamiq.com/) was used to create all of the wireframes during the design phase of this site.

These can be found using [this link](https://github.com/10xOXR/2BN_Savoury_Sensations/tree/master/design/wireframes).

##### back to [top](#table-of-contents)

---

## Features

As well as all of the features that were specified in the project brief, I have implemented several additional features the provide an enhanced user experience and better overall functionality.
 
### Existing Features

**Status-dependant Navbar**

The options that a user will see displayed in the navbar are dependant on whether or not they are logged in.
- Users that are not logged in will see:
    - Home
    - Browse Recipes
    - Search
    - Sign Up
    - Log In
- Users that are signed into the site will see:
    - Home
    - Browse Recipes
    - Search
    - Add Recipe
    - Logout

These differences are also reflected in the mobile version of the menu.

**Homepage Recipe Carousel**

The home/landing page for the site features a Materialize carousel, which displays the details of five randomly selected recipes from the database.

These recipes are chosen using the ```$sample``` function of MongoDB, which takes a random sample of the entries in the database and returns them to the cursor. The primary disadvantage of this method is that this function doesn't check if the next record it selects for inclusion in the sample has already been selected, leading to possible duplicates appearing in the carousel. If the number of records in the database is sufficiently large compared to the sample size then this is unlikely to be much of an issue.

**Create Account**

Users are able to create their own user account. The code checks against existing users in the database to ensure that the selected username is unique, and that both the username and password meet the minimum/maximum length requirements. The Werkzeug package takes the input from the password form and generates a SHA256 hash that is then stored in the user's profile in MongoDB. This provides far greater security than storing passwords in plain text. 

**User Profile Page**

Upon registering or logging into the site, users are directed to their own profile page. Here they can see their randomly generated profile picture that will be displayed against every recipe that they create, an option to change their password, an option to delete their account entirely, and a tabbed section displaying their favourite/own recipes.

**Change existing password**

Users are given the option to change their existing password via 'Change Password' button on the profile page. The app checks that their existing password is valid before generating a new SHA256 hash for their new password and storing this in the database.

**Delete user accounts**

Users have the option to completely delete their account via a button below their profile picture. Clicking this will launch a modal asking them if they are sure, and require them to confirm their password before proceeding. Users are also asked if they wish to also delete all of their recipes along with their account. Should they do so, all of the user's recipes are removed, and they are also removed from the saved favourites of all other registered users of the site. If they choose to leave their recipes on the site (default option) then the recipe author field for each of the user's recipes is updated to reflect the Admin account. The favourite count integer for each recipe that the use had in their database is decremented by one, the user's session is terminated, their record deleted from the database, and they are then redirected to the landing page.

**Logout**

Users that have logged into the site may end their session at any time by clicking the 'Logout' button on the navbar. Flask ends their session using the ```session.pop()``` method and redirects the user to the homepage.

**Browse Recipes**

All users are able to browse the recipes that have been submitted to the site, whether they are registered users or simply guests. The default sorted order of the recipes is by descending order of views, however users are able to change this via a dropdown to sort either by descending number of favourites, or alphabetically. Recipes are displayed to users as Materialize cards, each displaying the recipe picture (or a default image if none was provided), the recipe name (acting as a link to the full recipe detail), a direct link to view the recipe, and information showing how many views the recipe has and how many users have added the recipe to their favourites. Clicking the recipe image reveals more information about the recipe in the form of a short description.

**Recipe Detail Page**

When users click the link on the recipe card, they are taken to the recipe detail page. Here they are presented with the full details of the recipe, including all of the ingredients that they will require, the steps needed to prepare the recipe, information on the total time  and cooking temperatures required, and details of any allergens that may be present. They will also see the recipe's author and user profile picture. At the bottom of the page the user will be presented with a number of buttons depending on whether or not they are logged in.
- If browsing as a guest, they will only see a 'Go Back' button. 
- If they are logged in abut did not create the recipe that they are viewing, then they will also see either an 'Add Favourite' or 'Remove Favourite' button, depending on whether they have previously saved the recipe to their favourites.
- If they are also the user that created the recipe, they will see both an 'Edit' and 'Delete' button.

Each time a recipe is viewed, the app will increment the recipe's 'Views' field in the database by one.

**Add Recipes**

Registered users that are logged into the site are able to add new recipes to the database via the 'Add Recipe' page. They are asked to enter:
- Cuisine and Course types via dropdown menus (populated from the database).
- Recipe name*
- Description*
- Ingredients (each on a new line)*
- Preparation steps (each on a new line)*
- Prep Time in minutes*
- Cooking time in minutes*
- Temperature in Celsius*
- All possible allergens that the recipe may contain via a dropdown menu (populated from the database).
- A URL for the image that the user wishes to have displayed with their recipe. If none is provided, then a default will be displayed each time the recipe is viewed.

Fields with an asterisk are required. Recipe Name and Description fields also have minimum character limits.

Once the user has entered the required information and saved the recipe, they are immediately redirected to the Recipe Detail page for the recipe, where a Flash message informs them that their recipe was successfully added.

**Edit Recipes**

Users that have created a recipe are able to edit their creation by clicking the 'Edit' button that will be displayed to them in the 'Recipe Detail' page. This button will only appear if their username matches the one stored in the 'author' field in the recipe database record.

An identical form to the one that they saw on the 'Add Recipe' page will be displayed, but all fields will be pre-populated with the details from the recipe record. Users are then free to make any changes that they require.

Clicking the 'Update Recipe' button will write the changes to the database and redirect the user to the Recipe Detail page, where a Flash message will inform the user that their changes were successful.

**Delete Recipes**

Users may choose to delete any recipe that they have created by clicking the 'Delete' button from the Recipe Detail page.

Once clicked, a modal will appear asking if they are sure and reminding them that this action cannot be undone. If they proceed, the recipe is deleted from the database, and its ObjectID is removed from their list of recipes in their user record. The recipe is also removed from the favourites of all other users.

**Search Recipes**

Users are able to search through all of the recipes stored in the database using the Search Recipes page.

Users can search by keywords, cuisine type, or course types, and can filter out any specific allergens from their search. The keyword search is an ```AND``` search, where results are excluded as the search becomes more specific. The default search behaviour of searching in MongoDB is an ```OR``` search, which would have returned more and more results with every keyword entered.

**Pagination**

In both the Browse Recipes and Search pages, returned results are limited to eight recipe cards per page in order to not overload the user with too many results. Pagination has been implemented to let users move through all the results that available. Users are advised on each page the current range pf recipes that they are viewing ("Showing x - x of x recipes").

### Features Left to Implement

**Recipe Comments**

I would like to have implemented the ability of registered users to leave comments/reviews for each recipe, and for each comment to be up/down-voted by other users depending on their usefulness. Users would have the option of sorting the comments by newest/oldest or up-votes.

##### back to [top](#table-of-contents)

---

## Technologies Used

- [Microsoft Visual Studio Code](https://code.visualstudio.com/) - Open source IDE from Microsoft that was used to code this project.
- [GitHub](https://github.com/) - Remote repository for all project code with git version control.
- [TinyPNG](https://tinypng.com/) - Compresses images used on the site to keep file sizes to a minimum.

### Front-End Technologies

- [HTML](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) - The fundamental code structure for all webpages.
- [Sass CSS](https://sass-lang.com/) - CSS extension language used to build the CSS for this project and the recommended method to alter the default CSS of the Materialize framework.
- [jQuery 3.3.1](https://code.jquery.com/jquery/) - Javascript framework used to implement custom code and initialize Materialize functions.
- [Materialize 1.0.0](https://materializecss.com/) - Primary visual framework for this project, based on Google's Material Design.


### Back-End Technologies

- **Flask**
    - [Flask 1.0.2](http://flask.pocoo.org/) - A templating microframework used to dynamically build the pages in this project.
    - [Flask Blueprints](http://flask.pocoo.org/docs/1.0/blueprints/) - Allows Flask routes file to be broken into smaller route files. This enables more efficient debugging and keeps related routes together in their own files to improve readability of the code.
    - [Flask Talisman](https://github.com/GoogleCloudPlatform/flask-talisman) - Forces the use of HTTPS headers on all pages when the project is run in a production environment, as well as implements a Content Security Policy for greater over site security.
    - [Jinja 2.10](http://jinja.pocoo.org/docs/2.10/) - HTTP templating language for Python.
    - [Werkzeug 0.14](https://werkzeug.palletsprojects.com/en/0.14.x/) - Werkzeug is a comprehensive WSGI web application library. Installed as a dependency of Flask, it provides password hashing and checking for this project.
- **Heroku**
    - [Heroku](https://www.heroku.com) - Hosts the deployed version of this project.
- **Python**    
    - [Python 3.7.3](https://www.python.org/) - Python is an interpreted, high-level, general-purpose programming language and is the language used for all backend functions of this project.
    - [MongoDB Atlas](https://www.mongodb.com/) - MongoDB Atlas is the online host for remote MongoDB's NoSQL document-oriented databases.
    - [PyMongo 3.8.0](https://api.mongodb.com/python/current/) - PyMongo is a Python distribution containing tools for working with MongoDB.
    - [Python dotenv](https://github.com/theskumar/python-dotenv) - Reads the values of the environmental variables that are set in the project's `.env` file.


##### back to [top](#table-of-contents)

---

## Testing

Owing to time constraints, it was not possible to design and implement automatic Unit-testing for this project, and so extensive manual testing was completed instead.

An MS Excel workbook detailing these tests can be found [here](https://github.com/10xOXR/2BN_Savoury_Sensations/blob/master/tests/page_tests.xlsx). 

### Validators

**HTML**

Passing the HTML from all templates and base into the [W3C Markup Validator](https://validator.w3.org/) generates numerous errors, but these are expected as the validator is unable to understand the Jinja2 templating that builds most aspects of the page. For the HTML that does not involve Jinja2, no errors have been found.

**CSS**

The CSS for the project has been generated by the Sass CSS extension language. Passing the generated CSS through the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) shows that there are no errors. A number of warnings are flagged, but these relate to MS-Grid vendor prefixes and can be safely ignored.

**Javascript**

All Javascript was passes throught the [Esprima Syntax Validator](http://esprima.org/demo/validate.html) and was found to be syntactically valid.

**Python**

All Python code was passed through the [PEP8 Online](http://pep8online.com/) validator and is fully PEP8 compliant.

### Compatibility

The project was tested to ensure full usability across the following browsers and their mobile equivalents (where applicable):

- Chrome *v.74*
- Edge *v.18*
- Firefox *v.67*
- Safari *v.12*
- Opera *v.56*
- Internet Explorer *v.11*

##### back to [top](#table-of-contents)

---

## Deployment

### Local Deployment

Before you are able to deploy and run this application locally, you must have the following installed on your system:

- [Python3](https://www.python.org/downloads) to run the application.
- [PIP](https://pip.pypa.io/en/stable/installing) to install all app requirements.
- An IDE of your choice, such as [Microsoft Visual Studio Code](https://code.visualstudio.com).
- [GIT](https://www.atlassian.com/git/tutorials/install-git) for cloning and version control.
- [MongoDB CLI](https://www.mongodb.com) to develop your own database either locally or remotely on MongoDB Atlas.

Next, perform the following steps:

Clone this GitHub repository by either clicking the green *Clone or download* button and downloading the project as a zip-file (remember to unzip it first), or by entering the following into the Git CLI terminal:
    - `git clone https://github.com/10xOXR/2BN_Savoury_Sensations.git`.
- Navigate to the correct file location after unpacking the files.
    - `cd <path to folder>`
- Create a `.env` file containing your *MONGO_URI* and *SECRET_KEY* environmental variables.
- Create a `.flaskenv` file and add the following entries:
    - `FLASK_APP=run.py`
    - `FLASK_ENV=development`
- Install all requirements from the [requirements.txt](https://github.com/TravelTimN/ci-milestone04-dcd/blob/master/requirements.txt) file using this command:
    - `sudo -H pip3 -r requirements.txt`
- Sign up for a free account on [MongoDB](https://www.mongodb.com) and create a new Database called **m4RecipesCollection**. The *Collections* in that database should be as follows:

```
allergens
_id: <ObjectId>
allergenType: <array>

courses
_id: <ObjectId>
courseType: <array>

cuisines
_id: <ObjectId>
cuisineType: <array>

recipes
_id: <ObjectId>
cuisineType: <string>
courseType: <string>
recipeName: <string>
recipeDesc: <string>
ingredients: <array>
prepSteps: <array>
prepTime: <string>
cookTime: <string>
temp: <string>
allergens: <array>
imgUrl: <string>
author: <string>
views: <int32>
favourites: <int32>

users
_id: <ObjectId>
username: <string>
username_lower: <string>
password: <string>
user_img: <string>
user_recipes: <array>
user_favs: <array>
```

- At the terminal prompt, type ```flask run```. Flask should now start running a development server from 'http://127.0.0.1:5000'. Copy and paste this address to your browser and you should now see the project running.

### Remote Deployment

To implement this project on Heroku, the following must be completed:

1. Create a **requirements.txt** file so Heroku can install the required dependencies to run the app.
    - `sudo pip3 freeze --local > requirements.txt`
    - My file can be found [here](https://github.com/10xOXR/2BN_Savoury_Sensations/blob/master/requirements.txt).
2. Create a **Procfile** to tell Heroku what type of application is being deployed, and how to run it.
    - `echo web: python run.py > Procfile`
    - My file can be found [here](https://github.com/10xOXR/2BN_Savoury_Sensations/blob/master/Procfile).
3. Sign up for or log into your Heroku account, create your project app, and click the **Deploy** tab. Select *Connect GitHub* as the Deployment Method, and select *Enable Automatic Deployment*.
4. In the Heroku **Settings** tab, click on the *Reveal Config Vars* button to configure environmental variables as follows:
    - **IP** : `0.0.0.0`
    - **PORT** : `8080`
    - **MONGO_URI** : `<link to your Mongo DB>`
    - **SECRET_KEY** : `<your own secret key>`
5. The app will now be deployed and built by Heroku and will be ready to run.



##### back to [top](#table-of-contents)

---

## Credits

### Content

- [*"How to Write a Git Commit Message"*](https://chris.beams.io/posts/git-commit/) by **Chris Beams** (*as recommended by Code Institute assessors on previous projects*)
- [*BBC Good Food*](https://www.bbcgoodfood.com/recipes) for the recipes featured in this project


### Media

- All recipe images are from [*BBC Good Food*](https://www.bbcgoodfood.com/recipes)
- Background image used on the project was from [Pexels.com](https://www.pexels.com/)


### Acknowledgements

- My mentor, [Mark Railton](https://github.com/railto), for all of his input on this project.
- [Tim Nelson](https://github.com/TravelTimN), for the immeasurable patience and help that he always provides and being the sounding board for my ideas and solutions to issues. HDL.

##### back to [top](#table-of-contents)