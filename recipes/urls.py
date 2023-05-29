from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('index/<int:user_pk>', views.index, name='index'),
    path('create/<int:user_pk>/<str:ingr_check>', views.create, name='create'),
    path('ingredient_handler/<int:user_pk>/<str:action>',views.ingredient_handler, name='ingredient_handler'),
    path('view_recipe/<int:user_pk>/<int:rec_pk>', views.view_recipe, name='view_recipe'),
    path('edit_recipe/<int:user_pk>/<str:rec_pk>', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<str:rec_pk>', views.delete_recipe, name='delete_recipe'),
    path('recipe_scraper/<str:user_pk>', views.recipe_scraper, name='recipe_scraper'),
    path('register', views.register, name='register'),
    path('logout/<int:user_pk>', views.logout_request, name='logout'),
    path('login', views.login_request, name='login'),
]
