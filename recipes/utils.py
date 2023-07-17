from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from .models import Category, Recipe
from .forms import RecipeForm

UUID_LEN = 36

def get_new_cat(request):

    # get fields ready
    user = request.user 
    name = request.POST.get('new_category')
    image = request.POST.get('cat_image')
    description = request.POST.get('cat_description')

    # create new category and return to function to be saved
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
    # not going to fuck around with error handling now. this fixes it
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
    # not going to fuck around with error handling now. this fixes it
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

def create_recipe_no_cat(user_pk, request):

    # this bit of code is because no error handling was implemented for when no servings were given
    # not going to fuck around with error handling now. this fixes it
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
    recipe = Recipe(
               user=user,
               title=title,
               body = body,
               servings=servings,
               ingredients=ingredients)

    return recipe

def edit_recipe_new_cat(request, recipe):

    # this bit of code is because no error handling was implemented for when no servings were given
    # not going to fuck around with error handling now. this fixes it
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
    # not going to fuck around with error handling now. this fixes it
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

def edit_recipe_no_cat(request, recipe):

    # this bit of code is because no error handling was implemented for when no servings were given
    # not going to fuck around with error handling now. this fixes it
    if not request.POST.get('servings'):
        servings = 1
    else:    
        servings = request.POST.get('servings')

    recipe.title = request.POST.get('title')
    recipe.body = request.POST.get('body')
    recipe.servings = servings
    recipe.ingredients = request.POST.get('ingredients')

    return recipe

def scrape_recipe_new_cat(user_pk, request, online_recipe):
    
    # create and save new category
    new_cat = get_new_cat(request)
    new_cat.save()
    
    # create recipe and return to view
    recipe = scrape_recipe(user_pk, request, online_recipe, new_cat)
    return recipe

def scrape_recipe(user_pk, request, online_recipe, new_cat):
    
    # check if new category
    if new_cat:
        category = new_cat
    else:
        category_pk = request.POST.get('category')
        category = Category.objects.get(pk=category_pk)    

    # get the fields ready   
    user = User.objects.get(pk=user_pk)
    title = online_recipe.title()
    servings = int(online_recipe.yields()[0])
    site = online_recipe.host()

    # format list of ingredients to html string
    ingredients = ''
    for i, ingr in enumerate(online_recipe.ingredients(), 1):
        if i == 1:
            ingredients += f'<ul><li>{ingr}</li>'
        elif i == len(online_recipe.ingredients()):
            ingredients += f'<li>{ingr}</li></ul>'
        else:
            ingredients += f'<li>{ingr}</li>'        

    # format the body
    body_len = len(online_recipe.instructions_list())    
    if body_len < 7:
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

def collect_data(request):    
    if request.POST.get('category'):
        data = {'category': request.POST.get('category'),
                'title': request.POST.get('title'),
                'body': request.POST.get('body'),
                'servings': request.POST.get('servings'),
                'ingredient': request.POST.get('ingredient')}
    elif request.POST.get('new_category'):
        data = {'category': request.POST.get('new_category'),
                'title': request.POST.get('title'),
                'body': request.POST.get('body'),
                'servings': request.POST.get('servings'),
                'ingredient': request.POST.get('ingredient')} 
    else:
        data = {'title': request.POST.get('title'),
                'body': request.POST.get('body'),
                'servings': request.POST.get('servings'),
                'ingredient': request.POST.get('ingredient')}       
    
    return data

# manipulate the ingredients of the recipe
# the action argument lets the function know what action is to be taken
# this function returns the newly edited and saved recipe.
# in the case that no action was taken, it returns an http response
def ingredient_handler(request, action):
    user_pk = request.user.pk
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)

    # if recipe pk has been given it means we need to edit current recipe as apposed to creating a new one
    if len(action) > UUID_LEN:
        recipe_pk = action.split(',')[-1]
        action = action.split(',')[0]
        recipe = Recipe.objects.get(pk=recipe_pk)
        ingredient_list = recipe.ingredients.split('#')
        ingredient = request.POST.get('ingredient')
        if ingredient:
            if 'add' in action:
                ingredient_list.append(ingredient)
                ingredient_string = '#'.join(ingr for ingr in ingredient_list)
                recipe.ingredients = ingredient_string
                recipe.save()

                return recipe
            
            if 'header' in action:
                ingredient_list.append(f'!{ingredient.capitalize()}')
                ingredient_string = '#'.join(ingr for ingr in ingredient_list)
                recipe.ingredients = ingredient_string
                recipe.save()

                return recipe
                
        if 'del' in action:
            if ingredient_list:
                del ingredient_list[-1]
                ingredient_string = '#'.join(ingr for ingr in ingredient_list)       
                recipe.ingredients = ingredient_string
                recipe.save()

                return recipe           
        else:
            return recipe              
    else:

        # first time creating this recipe
        ingredient = request.POST.get('ingredient')
        if ingredient:
            ingredient_list = []
            if 'add' in action:                
                ingredient_list.append(ingredient)
                recipe = create_recipe_no_cat(user_pk, request, ingredient_list)
                recipe.save()

                return recipe
                                
            elif 'header' in action:
                ingredient_list.append(f'!{ingredient.capitalize()}')
                recipe = create_recipe_no_cat(user_pk, request, ingredient_list)
                recipe.save()

                return recipe                        

        data = collect_data(request)
        rec_form = RecipeForm(initial=data)
        ingredient_list = []

        return render(request, 'recipes/create.html', {
                    'rec_form': rec_form,
                    'ingr_list': ingredient_list,
                    'categories': categories,
                    'recipes': recipes,
                })
















