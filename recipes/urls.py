from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('index', views.index, name='index'),
    path('create/<str:ingr_check>', views.create, name='create'),
    path('ingredient_handler/<str:action>',views.ingredient_handler, name='ingredient_handler'),
    path('view_recipe/<int:rec_pk>', views.view_recipe, name='view_recipe'),
    path('edit_recipe/<str:rec_pk>', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<str:rec_pk>', views.delete_recipe, name='delete_recipe'),
    path('get_recipe', views.get_recipe, name='get_recipe'),
    path('register', views.register, name='register'),
    path('logout', views.logout_request, name='logout'),
    path('login', views.login_request, name='login'),
]
