from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from recipe_scrapers import scrape_me

from .forms import RecipeForm, IngredientForm, ScraperForm
from .models import Recipe, Category

INGREDIENT_LS = []

# view for creating new recipe
def create(request, ingr_check):
    if ingr_check == 'new':
        INGREDIENT_LS.clear()
    # handle for RecipeForm submission
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():

            # check if new category was given
            new_category = request.POST.get('new_category')

            # handle for new category
            if new_category:
                cat_image = request.POST.get('cat_image')
                cat_desctiption = request.POST.get('cat_description')
                c = Category(name=new_category, image=cat_image,
                             description=cat_desctiption)
                c.save()
                title = request.POST.get('title')
                body = request.POST.get('body')
                servings =request.POST.get('servings')

                # list of ingredients is stored as a comma seperated string in Recipe.ingredients
                # here we create the string to be stored
                ingr_str = ''
                for i in INGREDIENT_LS:
                    ingr_str += f'{i}#'

                # create and save new recipe object
                r = Recipe(category=c,
                           title=title,
                           body=body,
                           ingredients=ingr_str,
                           servings=servings)
                r.save()

                # clear ingredient list and update list of recipes and categories
                # so new recipe is available in navbar dropdown
                INGREDIENT_LS.clear()
                categories = Category.objects.all()
                recipes = Recipe.objects.all()

                return redirect(reverse('recipes:view_recipe', kwargs={'pk': r.pk}))

            # handle for if no new category was given
            else:
                category_pk = request.POST.get('category')
                category = Category.objects.get(pk=category_pk)
                title = request.POST.get('title')
                body = request.POST.get('body')
                servings = request.POST.get('servings')

                # list of ingredients is stored as a comma seperated string in Recipe.ingredients
                # here we create the string to be stored
                ingr_str = ''
                for i in INGREDIENT_LS:
                    ingr_str += f'{i}#'

                # create and save new recipe object
                r = Recipe(category=category,
                           title=title,
                           body=body,
                           ingredients=ingr_str,
                           servings=servings)
                r.save()

                # clear ingredient list and update list of recipes so new recipe is available in the navbar dropdown
                INGREDIENT_LS.clear()
                recipes = Recipe.objects.all()

                return redirect(reverse('recipes:view_recipe', kwargs={'pk': r.pk}))

        # error message if neither an existing category nor new category was given
        else:
            messages.info(request, 'Choose a category or create a new one.')
            return redirect(reverse('recipes:create', kwargs={'ingr_check': 'not_new'}))

    # set up initial forms, this view uses two forms: one for getting new ingredients and one for the recipe as a whole
    # set up lists of all categories and recipes. this is used to display the categories -> recipes in dropdown menus in navbar
    # this will happen in most views so i wont comment it every time
    ingr_form = IngredientForm()
    rec_form = RecipeForm(initial={'servings': 1})
    categories = Category.objects.all()
    recipes = Recipe.objects.all()

    return render(request, 'recipes/create.html', {
        'rec_form': rec_form,
        'ingr_form': ingr_form,
        'ingr_list': INGREDIENT_LS,
        'categories': categories,
        'recipes': recipes,
    })

# view for manipulating the global INGREDIENT_LIST, 
# the action argument lets the handler know what action is to be taken
def ingredient_handler(request, action):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = request.POST.get('ingredient')
            if 'add' in action:
                INGREDIENT_LS.append(ingredient)
            # '!' gets added to the beginning of the ingredient. when parsing the list in the template,
            # the '!' idicates that it is a header and it will be printed in bold
            elif 'header' in action:
                INGREDIENT_LS.append(f'!{ingredient.capitalize()}')
        if 'del' in action:
            if INGREDIENT_LS:
                del INGREDIENT_LS[-1]

    # when the INGREDIENT_LS gets manipulated in the edit.html template, the recipe pk gets appended to the end of the 'action'
    # this is handy because we need to update and save the ingredients for this recipe before the redirect
    # we also need to serve the recipe pk as an argument for the redirect
    if action[-1].isnumeric():
        recipe_pk = action.split(',')[-1]
        recipe = Recipe.objects.get(pk=recipe_pk)
        ingr_str = ''
        for i in INGREDIENT_LS:
            ingr_str += f'{i}#'
        recipe.ingredients = ingr_str
        recipe.save()
        return redirect(reverse('recipes:edit_recipe', kwargs={'pk': recipe_pk}))
    
    return redirect(reverse('recipes:create', kwargs={'ingr_check': 'not_new'}))

# initial 'homepage' for the site. this view displays clickable cards for each category
def index(request):
    categories = Category.objects.all()
    recipes = Recipe.objects.all()

    # when a recipe has been deleted, the user gets redirected to the index page
    # sometimes that means that a category will be empty
    # here we check if a category is empty, and if it is, delete it
    for cat in categories:
        empty_cat = True
        for rec in recipes:
            if rec.category.pk == cat.pk:
                empty_cat = False
        if empty_cat:
            cat_del = Category.objects.get(pk=cat.pk)
            cat_del.delete()

            # update list of categories to reflect the deleted one
            categories = Category.objects.all()

    return render(request, 'recipes/index.html', {
        'categories': categories,
        'recipes': recipes,
    })

# after clicking on a category on the index page, you are taken to this view which displays an unordered list
# of all recipes in said category
def view_cat(request, pk):
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
    cat_recipes = Recipe.objects.filter(category__pk=pk)

    return render(request, 'recipes/view_cat.html', {
        'cat_recipes': cat_recipes,
        'categories': categories,
        'recipes': recipes,
    })

# view for viewing a recipe
def view_recipe(request, pk):
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
    recipe = Recipe.objects.get(pk=pk)
    ingr_list = recipe.ingredients.split('#')[:-1]

    return render(request, 'recipes/view_recipe.html', {
        'recipe': recipe,
        'ingr_list': ingr_list,
        'categories': categories,
        'recipes': recipes,
    })

# view for editing a recipe
# I realise this view looks a lot like the create view and thus contains a lot of redundancy
# initially i did try and handle for editing the recipe in the create view, but i just couldn't get it to work
def edit_recipe(request, pk):
    # handle for RecipeForm submission
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():

            # get the specific recipe to be edited by pk
            recipe = Recipe.objects.get(pk=pk)

            # check if new category has been given and handle accordingly
            new_category = request.POST.get('new_category')
            if new_category:
                cat_image = request.POST.get('cat_image')
                cat_description = request.POST.get('cat_description')
                c = Category(name=new_category, image=cat_image, description=cat_description)
                c.save()

                # update list of categories so new category is available in navbar
                categories = Category.objects.all()

                # update fields of edited recipe
                recipe.category = c
                recipe.title = request.POST.get('title')
                recipe.body = request.POST.get('body')
                recipe.servings = request.POST.get('servings')
                ingr_str = ''

                # list of ingredients is stored as a comma seperated string in Recipe.ingredients
                # here we create the string to be stored
                for i in INGREDIENT_LS:
                    ingr_str += f'{i}#'
                recipe.ingredients = ingr_str

                # save recipe, clear INGREDIENT_LS and serve redirect to view of newly updated recipe
                recipe.save()
                INGREDIENT_LS.clear()
                return redirect(f'/view_recipe/{recipe.pk}')

            # handle for if no new category was given
            else:
                category_pk = request.POST.get('category')
                category = Category.objects.get(pk=category_pk)
                recipe.category = category
                recipe.title = request.POST.get('title')
                recipe.body = request.POST.get('body')
                recipe.servings = request.POST.get('servings')
                ingr_str = ''

                for i in INGREDIENT_LS:
                    ingr_str += f'{i}#'
                recipe.ingredients = ingr_str
                # save recipe, clear INGREDIENT_LS and serve redirect to view of newly updated recipe

                recipe.save()
                INGREDIENT_LS.clear()
                return redirect(f'/view_recipe/{recipe.pk}')

        # error message for if no category was given
        else:
            messages.info(request, 'Choose a category or create a new one.')
            return redirect(reverse('recipes:edit_recipe', kwargs={'pk': pk}))

    else:
        categories = Category.objects.all()
        recipes = Recipe.objects.all()

        # get the specific recipe by pk to populate RecipeForm with initial data to be edited
        recipe = Recipe.objects.get(pk=pk)

        # if INGREDIENT_LS is empty, populate it with data from recipe.ingredients
        # it is important to check if the list is empty first or else this code will run 
        # every time the user is redirected to this view
        if not INGREDIENT_LS:
            for ing in recipe.ingredients.split('#')[:-1]:
                INGREDIENT_LS.append(ing)

        data = {'category': recipe.category,
                'title': recipe.title,
                'body': recipe.body,
                 'servings': recipe.servings }

        rec_form = RecipeForm(initial=data)
        ingr_form = IngredientForm()

        return render(request, 'recipes/edit.html', {
            'categories': categories,
            'recipes': recipes,
            'rec_form': rec_form,
            'ingr_list': INGREDIENT_LS,
            'ingr_form': ingr_form,
            'recipe': recipe,
        })

# simple view for deleting a recipe
def delete_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe.delete()
    INGREDIENT_LS.clear()
    return redirect('recipes:index')

# lets scrape some recipes!
def recipe_scraper(request):
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            recipe_url = request.POST.get('url')
            try:
                online_recipe = scrape_me(recipe_url, wild_mode = True)                    
                # check if new category is given
                new_category = request.POST.get('new_category')
                # create and save new category
                if new_category:
                    cat_image = request.POST.get('cat_image')
                    cat_description = request.POST.get('cat_description')
                    c = Category(name=new_category, image=cat_image, description=cat_description)
                    c.save()
                    ingr_str = ''
                    for i in online_recipe.ingredients():
                        ingr_str += f'{i}#'
                    online_title = online_recipe.title()
                    servings = int(online_recipe.yields()[0])
                    site = online_recipe.host()
                    if len(online_recipe.instructions_list()) < 7:
                        formatted_body = ''
                        step_count = 1
                        for instruction in online_recipe.instructions_list():
                            formatted_body += f'<strong><small>Step {step_count}</small></strong><br>{instruction} <br /><br />'
                            step_count += 1
                    else:
                        formatted_body = ''
                        for instruction in online_recipe.instructions_list():
                            formatted_body += f'<li>{instruction} <br /><br />'        
                    r = Recipe(title =online_title, category=c, body=formatted_body, ingredients=ingr_str, servings=servings, site=site)
                    r.save()
                    return  redirect(reverse('recipes:view_recipe', kwargs={'pk': r.pk})) 
                else:
                    cat_pk = request.POST.get('category')
                    c = Category.objects.get(pk=cat_pk)
                    ingr_str = ''
                    for i in online_recipe.ingredients():
                        ingr_str += f'{i}#'
                    online_title = online_recipe.title()
                    servings = int(online_recipe.yields()[0])
                    site = online_recipe.host()
                    if len(online_recipe.instructions_list()) < 9:
                        formatted_body = ''
                        step_count = 1
                        for instruction in online_recipe.instructions_list():   
                            formatted_body += f'<strong><small>Step {step_count}</small></strong><br>{instruction} <br /><br />'
                            step_count += 1
                    else:
                        formatted_body = ''
                        for instruction in online_recipe.instructions_list():
                            formatted_body += f'<li>{instruction} <br /><br />'         
                    
                    r = Recipe(title =online_title, category=c, body=formatted_body, ingredients=ingr_str, servings=servings, site=site)
                    r.save()
                    return  redirect(reverse('recipes:view_recipe', kwargs={'pk': r.pk}))
                
            except:
                messages.error(request, 'Something went wrong. It is likely that this URL does not contain a recipe')
                return redirect('recipes:recipe_scraper') 


    form = ScraperForm()
    recipes = Recipe.objects.all()
    categories = Category.objects.all()
    return render(request, 'recipes/scraper.html', {
        'form': form,
        'recipes': recipes,
        'categories': categories
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipes:index')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
    form = UserCreationForm()
    return render(request, 'recipes/register.html', {
        'form': form,
    })
