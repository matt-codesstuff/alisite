from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from recipe_scrapers import scrape_me

from .forms import RecipeForm, IngredientForm, ScraperForm
from .models import Recipe, Category
from .helpers import *

INGREDIENT_LS = []

# homepage
def index(request):
    user_pk = request.user.pk
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)

    # check if a category is empty, and if it is, delete it
    if categories:
        for cat in categories:
            empty_cat = True
            for rec in recipes:
                if rec.category.pk == cat.pk:
                    empty_cat = False
            if empty_cat:
                cat_del = Category.objects.get(pk=cat.pk)
                cat_del.delete()

            # update list of categories to reflect deleted ones    
            categories = Category.objects.filter(user__pk=user_pk)    

    return render(request, 'recipes/index.html', {
        'categories': categories,
        'recipes': recipes,
    })


# creating new recipe
def create(request, ingr_check):
    user_pk = request.user.pk

    # ingr_ls needs to be cleared the first time we run this view
    if ingr_check == 'new':
        INGREDIENT_LS.clear()

    # set up initial forms, etc.
    ingr_form = IngredientForm()
    rec_form = RecipeForm(user=request.user, initial={'servings': 1})
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)

    # handle for RecipeForm submission
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():

            # check if new category was given
            new_category = request.POST.get('new_category')
            
            if new_category:

                # check if new category alredy exists
                category_names = [cat.name for cat in categories]
                if new_category in category_names:
                    messages.info(request, 'Category Already Exists')

                    data = {'category': request.POST.get('category'),
                            'title': request.POST.get('title'),
                            'body': request.POST.get('body'),
                            'servings': request.POST.get('servings'),}
                    
                    rec_form = RecipeForm(initial=data)
                    ingr_form = IngredientForm()

                    return render(request, 'recipes/create.html', {
                        'rec_form': rec_form,
                        'ingr_form': ingr_form,
                        'ingr_list': INGREDIENT_LS,
                        'categories': categories,
                        'recipes': recipes,
                    })

            # create recipe with new category            
                recipe = create_recipe_new_cat(user_pk, request, INGREDIENT_LS)
                recipe.save()
                INGREDIENT_LS.clear()

                return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))

            # create recipe with existing category
            else:
                recipe = create_recipe_existing_cat(user_pk, request, INGREDIENT_LS, categories)
                recipe.save()
                INGREDIENT_LS.clear()

                return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))

        # error message for if no category is given
        else:
            messages.info(request, 'Choose a category or create a new one.')

            data = {'title': request.POST.get('title'),
                    'body': request.POST.get('body'),
                    'servings': request.POST.get('servings'),}
            
            rec_form = RecipeForm(initial=data)
            ingr_form = IngredientForm()

            return render(request, 'recipes/create.html', {
            'rec_form': rec_form,
            'ingr_form': ingr_form,
            'ingr_list': INGREDIENT_LS,
            'categories': categories,
            'recipes': recipes,
        })

    return render(request, 'recipes/create.html', {
        'rec_form': rec_form,
        'ingr_form': ingr_form,
        'ingr_list': INGREDIENT_LS,
        'categories': categories,
        'recipes': recipes,
    })


# editing a recipe
def edit_recipe(request, rec_pk):
    user_pk = request.user.pk

    # retrieve recipe to be edited
    recipe = Recipe.objects.get(pk=rec_pk)

    # if INGREDIENT_LS is empty, populate it with data from recipe.ingredients
    # (if recipe.ingredients exists)
    if recipe.ingredients:
        if not INGREDIENT_LS:
            for ing in recipe.ingredients.split('#'):
                INGREDIENT_LS.append(ing)

    # gather data to populate form to be edited   
    data = {'category': recipe.category,
            'title': recipe.title,
            'body': recipe.body,
            'servings': recipe.servings
              }
    
    # set up forms etc.
    rec_form = RecipeForm(initial=data, user=request.user)
    ingr_form = IngredientForm()
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)

    # handle for form submission    
    if request.method == 'POST':
        form = RecipeForm(request.POST)        
        if form.is_valid():

            # check if new category is given           
            new_category = request.POST.get('new_category')

            # check if new category already exists
            category_names = [cat.name for cat in categories]
            if new_category in category_names:
                messages.info(request, 'Category Already Exists')
                data = {'category': request.POST.get('category'),
                        'title': request.POST.get('title'),
                        'body': request.POST.get('body'),
                        'servings': request.POST.get('servings')}
                
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
            
            # handle for new category
            if new_category:
                recipe = edit_recipe_new_cat(request, INGREDIENT_LS, recipe)
                recipe.save()           
                INGREDIENT_LS.clear()

                return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': rec_pk}))

            # handle for existing category
            else:               
                recipe = edit_recipe_existing_cat(request, INGREDIENT_LS, recipe)                
                recipe.save()
                INGREDIENT_LS.clear()

                return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': rec_pk}))

    return render(request, 'recipes/edit.html', {
        'categories': categories,
        'recipes': recipes,
        'rec_form': rec_form,
        'ingr_list': INGREDIENT_LS,
        'ingr_form': ingr_form,
        'recipe': recipe,
    })


# lets scrape some recipes!
def get_recipe(request):

    # set up forms etc.
    form = ScraperForm(user=request.user)
    user_pk = request.user.pk
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)

    # handle for form submission
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():            
            try:
                recipe_url = request.POST.get('url')
                online_recipe = scrape_me(recipe_url, wild_mode = True)                                   
                new_category = request.POST.get('new_category')

                # check if new category alredy exists
                category_names = [cat.name for cat in categories]
                if new_category in category_names:
                    messages.info(request, 'Category Already Exists')
                    return redirect(reverse('recipes:get_recipe', kwargs={'user_pk': user_pk}))
                
                # handle for new category
                if new_category:                   
                    recipe = scrape_recipe_new_cat(user_pk, request, online_recipe)
                    recipe.save()                   

                    return  redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))

                # handle for existing category 
                else:
                    recipe = scrape_recipe(user_pk, request, online_recipe, None)
                    recipe.save()

                    return  redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))
                
            except:
                messages.error(request, 'Something went wrong. It is likely that this URL does not contain a recipe')
                return redirect('recipes:get_recipe') 

    return render(request, 'recipes/get_recipe.html', {
        'form': form,
        'recipes': recipes,
        'categories': categories
    })
  
# manipulate INGREDIENT_LS
# the action argument lets the function know what action is to be taken
def ingredient_handler(request, action):
    if request.method == 'POST':
        form = IngredientForm(request.POST)

        # custom form validation written in forms.py fo ensure no empty string is appended to the list
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
    '''
    when the INGREDIENT_LS gets manipulated in the edit.html template, the recipe pk gets appended to the end of the 'action'
    this is handy because we need to update and save the ingredients for this recipe before the redirect
    we also need to serve the recipe pk as an argument for the redirect
    '''
    if action[-1].isnumeric():
        recipe_pk = action.split(',')[-1]
        recipe = Recipe.objects.get(pk=recipe_pk)
        ingr_str = '#'.join(ingr for ingr in INGREDIENT_LS)

        recipe.ingredients = ingr_str
        recipe.save()
        return redirect(reverse('recipes:edit_recipe', kwargs={'rec_pk': recipe_pk}))
    
    return redirect(reverse('recipes:create', kwargs={'ingr_check': 'not_new'}))


# viewing a recipe
def view_recipe(request, rec_pk):
    user_pk = request.user.pk
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)
    recipe = Recipe.objects.get(pk=rec_pk)
    if recipe.ingredients:
        ingr_list = recipe.ingredients.split('#')
    else:
        ingr_list = []    

    return render(request, 'recipes/view_recipe.html', {
        'recipe': recipe,
        'ingr_list': ingr_list,
        'categories': categories,
        'recipes': recipes,
    })


# deleting a recipe
def delete_recipe(request, rec_pk):
    recipe = Recipe.objects.get(pk=rec_pk)
    recipe.delete()
    INGREDIENT_LS.clear()
    return redirect('recipes:index')


# register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipes:index')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

    form = UserCreationForm()
    return render(request, 'recipes/register.html', {
        'form': form,
    })


# logout user
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('recipes:index')


# login user
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes:index')
            else:
                for msg in form.error_messages:
                    messages.error(request, form.error_messages[msg])
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])    

    form = AuthenticationForm()
    return render(request, 'recipes/login.html', {
        'form': form,
    })
