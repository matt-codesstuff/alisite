from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import Category, Recipe

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

def create_recipe_new_cat(user_pk, request, ingr_ls):

    # create and save new category
    new_cat = get_new_cat(request)   
    new_cat.save()

    # get fields ready
    user = User.objects.get(pk=user_pk)
    title = request.POST.get('title')
    body = request.POST.get('body')
    servings = request.POST.get('servings')
    ingr_string = '#'.join(ingr for ingr in ingr_ls)

    # create recipe and return to view to be saved
    recipe = Recipe(category=new_cat,
               user=user,
               title=title,
               body = body,
               servings=servings,
               ingredients=ingr_string)

    return recipe

def create_recipe_existing_cat(user_pk, request, ingr_ls, categories):

    # create recipe and return to view to be saved
    user = User.objects.get(pk=user_pk)
    category_pk = request.POST.get('category')
    category = Category.objects.get(pk=category_pk)
    title = request.POST.get('title')
    body = request.POST.get('body')
    servings = request.POST.get('servings')
    ingr_string = '#'.join(ingr for ingr in ingr_ls)

    recipe = Recipe(category=category,
            user=user,
            title=title,
            body = body,
            servings=servings,
            ingredients=ingr_string)

    return recipe 

def edit_recipe_new_cat(request, ingr_ls, recipe):
    
    # create and save new category
    new_cat = get_new_cat(request)
    new_cat.save()

    # edit recipe and return to view to be saved
    recipe.category = new_cat
    recipe.title = request.POST.get('title')
    recipe.body = request.POST.get('body')
    recipe.servings =request.POST.get('sercings')
    ingr_str = '#'.join(ingr for ingr in ingr_ls)
    recipe.ingredients = ingr_str

    return recipe

def edit_recipe_existing_cat(request, ingr_ls, recipe, categories):

    # edit recipe and return to view to be saved
    category_pk = request.POST.get('category')
    category = Category.objects.get(pk=category_pk)
    recipe.category = category
    recipe.title = request.POST.get('title')
    recipe.body = request.POST.get('body')
    recipe.servings = request.POST.get('servings')
    ingr_string = '#'.join(ingr for ingr in ingr_ls)
    recipe.ingredients = ingr_string

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
    ingr_str = '#'.join(ingr for ingr in online_recipe.ingredients())

    # format the body
    body_len = len(online_recipe.instructions_list())    
    if body_len < 7:
        formatted_body = ''
        step_count = 1
        for instruction in online_recipe.instructions_list():
            formatted_body += f'<strong><small>Step {step_count}</small></strong><br />{instruction} <br /><br />'
            step_count += 1
    else:
        formatted_body = '<ul>'
        for i, instruction in enumerate(online_recipe.instructions_list(), 1):
            if i == body_len:
                formatted_body += f'<li>{instruction}<br /><br/></ul>' 
            else:
                formatted_body += f'<li>{instruction}<br /><br />'              

    # create recipe and return to view to be saved        
    recipe = Recipe(user=user,
                title =title, 
                category=category, 
                body=formatted_body, 
                ingredients=ingr_str, 
                servings=servings, 
                site=site)
           
    return recipe












