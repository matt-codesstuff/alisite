# Ali's Kitchen - a Recipe Storage and  Management Application

This is a simple web application that allows a user to store, edit and view their recipes conveniently
 online. It uses the Python Django web-framework to create a CRUD (Create, Read, Update, Delete) back-end and uses HTML, CSS and Bootstrap to create a user-friendly, responsive front-end interface.

## Hosted
This app is hosted on https://aliskitchen-67f842b12558.herokuapp.com/

Use these credentials to log in:

Username: visitor 

Password: kitchen123 

## Features

- Easily create new recipes or edit existing ones using CKEditor (a WYSIWYG text-editor).
- Scrape recipes from your favourite websites to add to your collection.
- Easy access to all your recipes using the dropdown menus found on the home page as well as the nav-bar.
- Store recipes under categories for easy management.
- View your recipes without the clutter often found on online sites.

## Prerequisites

Before you can run this application, you need to have the following installed on your system:

- Python (3.8 or higher)
- Django (4.2 or higher)
- Git

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

5. Generate sceret key:

   ```bash
   python manage.py shell
   >>>from django.core.management.utils import get_random_secret_key
   >>>print(get_random_secret_key())
   >>>quit()
   ```
   
5. Copy secret key and paste it into the SECRET_KEY variable found at alisite\settings\common.py.
   The secret key needs to be a string, so remember to put quotes aound it.

  

7. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

8. Create a superuser to access the Django admin interface:

   ```bash
   python manage.py createsuperuser
   ```

9. Start the development server:

   ```bash
   python manage.py runserver
   ```

10. Access the application in your web browser at `http://127.0.0.1:8000/`.

## Usage

1. Click on "New" in the nav-bar to be taken to the New Recipe page. Here a user can enter the ingredients and body of their recipe in two seperate CKEditor text-editors. It is required that a category is given in order to save a new recipe. If no category exists yet, you can create a new category on this page.

2. "From The Internet" takes the user to the Recipe Scraper page. Simply paste a link to the recipe you want to scrape, choose a category and click on "Go!". The recipe gets scraped, formatted and stored to your database.
3. Clicking on a recipe from a dropdown menu takes you to the View Recipe page to view  your recipe.
4. On the bottom of every View Recipe page is an "Edit" button which allows you to edit the recipe. It is also possible to delete a recipe on the edit page.
5. Clicking on "Ali's Kitchen" in the nav-bar takes the user to the Home Page, which has neatly spaced cards for each category and dropdown menus for easy access to recipes.
6. Visit the admin interface at `http://127.0.0.1:8000/admin/` and log in with the superuser account you created earlier for a behind the scenes look at your database.


## Technologies Used:
Python, Django, SQLite, PostgreSQL, Bootstrap, HTML5, CSS, JavaScript, Git
