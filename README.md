# Ali's Kitchen - a Recipe Storage and  Management Application

This is a simple web application that allows a user to store, edit and view their recipes conveniently
 online. It uses the Python Django web-framework to create a CRUD (Create, Read, Update, Delete) back-end and uses HTML, CSS and Bootstrap to create a user-friendly front-end interface.

## Hosted
This site is hosted on https://aliskitchen-67f842b12558.herokuapp.com/ 

## Features

- Easily create new recipes or edit existing ones using CKEditor (a WYSIWYG text-editor).
- Scrape recipes from your favourite websites to add to your collection.
- Easy access to all your recipes using the dropdown menus found on the landing page as well as the nav-bar.
- Store recipes under categories for easy management.
- View your recipes without the clutter often found on online sites.

## Prerequisites

Before you can run this application, you need to have the following installed on your system:

- Python (3.7 or higher)
- Django
- Virtual environment (recommended)

## Getting Started

Follow these steps to get the application up and running on your local machine:

1. Clone this repository:

   ```bash
   git clone https://github.com/matt-codesstuff/alisite.git
   cd alisite
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser to access the Django admin interface:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the application in your web browser at `http://127.0.0.1:8000/`.

## Usage

1. The app requires a new user be created in order to use it. If you have already created a superuser, you can use the username and password used there to log in by clicking "Log in here". Click on "Register for new account here" to create a new user account

2. Click on "New" in the nav-bar to be taken to the New Recipe page. Here a user can enter the ingredients and body of their recipe in two seperate CKEditor text-editors. It is required that a category is given in order to save a new recipe. If no categories exist yet, you can create a new category on this page.

3. "From The Internet" takes the user to the Recipe Scraper page. Simply paste a link to the recipe you want to scrape, choose a category and click on "Go!". The recipe gets scraped, formatted and stored to your database.
4. Clicking on a recipe from a dropdown menu takes you to the View Recipe page to view  your recipe.
5. On the bottom of every View Recipe page is an "Edit" button which allows you to edit the recipe. It is also possible to delete a recipe on the edit page.
6. Clicking on "Ali's Kitchen" in the nav-bar takes the user to the Landing Page, which has neatly spaced cards for each category and dropdown menus for easy access to recipes.
7. Visit the admin interface at `http://127.0.0.1:8000/admin/` and log in with the superuser account you created earlier for a behind the scenes look at your database.


## Technologies Used:
Python, Django, MySQL, PostgreSQL, Bootstrap, HTML5, CSS, JavaScript
