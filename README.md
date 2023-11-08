# Alisite - a Recipe Storage and  Management Application

This is a simple web application that allows a user to store, edit and view their recipes conveniently
 online. It uses the Python Django web-framework to create a CRUD (Create, Read, Update, Delete) back-end and uses HTML, CSS and Bootstrap to create a user-friendly front-end interface.

## Features

- Easily create new recipes or edit existing ones using CKEditor (a WYSIWYG text-editor).
- Scrape recipes from your favourite websites to add to your collection.
- Easy access to all your recipes using the dropdown menus found on the landing page as well as the nav-bar.
- Store recipes under categories for easy management.
- View your recipes without the clutter ofen found on oline sites.

## Prerequisites

Before you can run this application, you need to have the following installed on your system:

- Python (3.7 or higher)
- Django
- Virtual environment (recommended)

## Getting Started

Follow these steps to get the application up and running on your local machine:

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/django-crud-app.git
   cd django-crud-app
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

1. Visit the admin interface at `http://127.0.0.1:8000/admin/` and log in with the superuser account you created earlier.

2. Use the admin interface to add, update, and delete records in the database.

3. Visit the main application at `http://127.0.0.1:8000/` to interact with the CRUD functionality via the user-friendly web interface.

## Customization

You can customize the application by modifying the HTML templates and CSS files located in the `templates` and `static` directories, respectively. Feel free to adjust the design and functionality to suit your needs.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Create a pull request on the original repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django community for creating an excellent web framework.
- Bootstrap for the responsive and appealing design.
- Your contributions and feedback are greatly appreciated!

Feel free to use this project as a starting point for your own Django-based CRUD web applications. If you have any questions or encounter issues, please open an [issue](https://github.com/your-username/django-crud-app/issues) on the GitHub repository.
