from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('ingredient_handler/<str:action>', views.ingredient_handler, name='ingredient_handler'),
    path('view_cat/<int:pk>', views.view_cat, name='view_cat'),
    path('view_cat/view_recipe/<int:pk>', views.view_recipe, name='view_recipe'),
    path('edit_recipe/<str:pk>', views.edit_recipe, name='edit_recipe'),

]
