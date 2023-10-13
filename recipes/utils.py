from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from .models import Category, Recipe
from .forms import RecipeForm


def get_new_cat(request):

    # get fields ready
    user = request.user 
    name = request.POST.get('new_category')
    image = request.POST.get('cat_image')
    description = request.POST.get('cat_description')

    # create new category and return to calling function to be saved
    category = Category(user=user,
                 name=name,
                 image=image,
                 description=description)
    return category

def create_recipe_new_cat(user_pk, request):

    # create and save new category
    new_cat = get_new_cat(request)   
    new_cat.save()

    # this bit of code is because no error handling was implemented for when no servings were given
    # **note to self:** handle for this error in the form
    if not request.POST.get('servings'):
        servings = 1
    else:    
        servings = request.POST.get('servings')

    # get fields ready
    user = User.objects.get(pk=user_pk)
    title = request.POST.get('title')
    body = request.POST.get('body')
    ingredients = request.POST.get('ingredients')

    # create recipe and return to view to be saved
    recipe = Recipe(category=new_cat,
               user=user,
               title=title,
               body = body,
               servings=servings,
               ingredients=ingredients)

    return recipe

def create_recipe_existing_cat(user_pk, request):

    # this bit of code is because no error handling was implemented for when no servings were given
    # not going to mess around with error handling now. this fixes it
    if not request.POST.get('servings'):
        servings = 1
    else:    
        servings = request.POST.get('servings')

    # create recipe and return to view to be saved
    user = User.objects.get(pk=user_pk)
    category_pk = request.POST.get('category')
    category = Category.objects.get(pk=category_pk)
    title = request.POST.get('title')
    body = request.POST.get('body')
    ingredients = request.POST.get('ingredients')

    recipe = Recipe(category=category,
            user=user,
            title=title,
            body = body,
            servings=servings,
            ingredients=ingredients)

    return recipe 

def edit_recipe_new_cat(request, recipe):

    # this bit of code is because no error handling was implemented for when no servings were given
    # not going to mess around with error handling now. this fixes it
    if not request.POST.get('servings'):
        servings = 1
    else:    
        servings = request.POST.get('servings')
    
    # create and save new category
    new_cat = get_new_cat(request)
    new_cat.save()

    # edit recipe and return to view to be saved
    recipe.category = new_cat
    recipe.title = request.POST.get('title')
    recipe.body = request.POST.get('body')
    recipe.servings = servings
    recipe.ingredients = request.POST.get('ingredients')

    return recipe

def edit_recipe_existing_cat(request, recipe):

    # this bit of code is because no error handling was implemented for when no servings were given
    # not going to mess around with error handling now. this fixes it
    if not request.POST.get('servings'):
        servings = 1
    else:    
        servings = request.POST.get('servings')

    # edit recipe and return to view to be saved
    category_pk = request.POST.get('category')
    category = Category.objects.get(pk=category_pk)
    recipe.category = category
    recipe.title = request.POST.get('title')
    recipe.body = request.POST.get('body')
    recipe.servings = servings
    recipe.ingredients = request.POST.get('ingredients')

    return recipe

def scrape_recipe_new_cat(user_pk, request, online_recipe):
    
    # create and save new category
    new_cat = get_new_cat(request)
    new_cat.save()
    
    # create recipe and return to view to be saved
    recipe = scrape_recipe(user_pk, request, online_recipe, new_cat)
    return recipe

def scrape_recipe(user_pk, request, online_recipe, new_cat=False):
    
    # get the fields ready
    if new_cat:
        category = new_cat
    else:    
        category_pk = request.POST.get('category')
        category = Category.objects.get(pk=category_pk)      
    user = User.objects.get(pk=user_pk)
    
    title = online_recipe.title()
    servings = int(online_recipe.yields()[0])
    site = online_recipe.host()
    
    # sometimes running the .ingredients() method returns an error
    # in that case, we get the ingredients from the object's raw data attribute
    try:
        ingredient_list = online_recipe.ingredients()
    except AttributeError:
        ingredient_list = online_recipe.schema.data['recipeIngredient']  
        
    # format list of ingredients into an html string
    # to be displayed in the ckeditor widget
    ingredients = ''
    for i, ingr in enumerate(ingredient_list, 1):
        if i == 1:
            ingredients += f'<ul><li>{ingr}</li>'
        elif i == len(ingredient_list):
            ingredients += f'<li>{ingr}</li></ul>'
        else:
            ingredients += f'<li>{ingr}</li>' 
                       
    # format the body to html string
    # if there are less than eight steps in the recipe, add a 'step count' header to each step
    # if it's eight steps or more, create a bulleted list of the steps
    body_len = len(online_recipe.instructions_list())    
    if body_len < 8:
        formatted_body = ''
        step_count = 1
        for instruction in online_recipe.instructions_list():
            formatted_body += f'<strong>Step {step_count}</strong><br />{instruction} <br /><br />'
            step_count += 1
    else:
        formatted_body = '<ul>'
        for i, instruction in enumerate(online_recipe.instructions_list(), 1):
            if i == body_len:
                formatted_body += f'<li>{instruction}</li></ul><br/>' 
            else:
                formatted_body += f'<li>{instruction}</li><br />'              
    
    # create recipe and return to view to be saved        
    recipe = Recipe(user=user,
                title =title, 
                category=category, 
                body=formatted_body, 
                ingredients=ingredients, 
                servings=servings, 
                site=site)
          
    return recipe

# collect data for re-populating forms
def collect_data(request):    
    data = {'category': request.POST.get('category'),
            'new_category': request.POST.get('new_category'),
            'title': request.POST.get('title'),
            'body': request.POST.get('body'),
            'servings': request.POST.get('servings'),
            'cat_image': request.POST.get('cat_image'),
            'cat_description': request.POST.get('cat_description'),
            'ingredients': request.POST.get('ingredients'),}
    
    return data

















