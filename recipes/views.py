from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from recipe_scrapers import scrape_me

from .forms import RecipeForm, ScraperForm
from .models import Recipe, Category
from .utils import *

UUID_LEN = 36

# homepage
def index(request):
    user_pk = request.user.pk
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)

    # some cleanup to find incomplete recepes or empty categories and delete them
    if recipes:
        for rec in recipes:
            if not rec.title or not rec.category or not rec.body:
                rec.delete()
                recipes = Recipe.objects.filter(user__pk=user_pk)
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
def create(request, action):

    # handle for ingredients
    if 'new' not in action and 'save' not in action:  
        recipe = ingredient_handler(request, action)
        if isinstance(recipe, HttpResponse):
            return recipe
        else:
            ingredient_list = recipe.ingredients.split('#')

    user_pk = request.user.pk  
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)   

    # handle for RecipeForm submission
    if 'save' in action:
        if request.method == 'POST':
            form = RecipeForm(request.POST)
            if form.is_valid():
                
                recipe_pk = action.split(',')[-1]
                recipe = Recipe.objects.get(pk=recipe_pk)
                ingredient_list = recipe.ingredients.split('#')

                # check if new category was given
                new_category = request.POST.get('new_category')            
                if new_category:

                    # check if new category alredy exists
                    category_names = [cat.name for cat in categories]
                    if new_category in category_names:
                        messages.info(request, 'Category Already Exists')

                        data = collect_data(request)
                        rec_form = RecipeForm(user=request.user, initial=data)

                        return render(request, 'recipes/create.html', {
                            'rec_form': rec_form,
                            'ingr_list': ingredient_list,
                            'categories': categories,
                            'recipes': recipes,
                            'recipe': recipe
                        })

                    # create recipe with new category       
                    recipe = create_recipe_new_cat(user_pk, request, ingredient_list)
                    recipe.save()

                    return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))
                
                # create recipe with existing category
                elif request.POST.get('category'):
                    recipe = create_recipe_existing_cat(user_pk, request, ingredient_list)
                    recipe.save()

                    return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))    

            # error message for incomplete recipe
            else:
                messages.info(request, 'Note: You must provide a title, category and body to save the recipe')

                if len(action) > UUID_LEN:
                    recipe_pk = action.split(',')[-1]
                    recipe = Recipe.objects.get(pk=recipe_pk)
                    ingredient_list = recipe.ingredients.split('#') 
                else:
                    recipe = ''
                    ingredient_list = []          
                    
                data = collect_data(request)               
                rec_form = RecipeForm(user=request.user, initial=data)

                return render(request, 'recipes/create.html', {
                'rec_form': rec_form,
                'recipe': recipe,
                'ingr_list': ingredient_list,
                'categories': categories,
                'recipes': recipes,
            })

    if action == 'new':
        recipe = ''
        ingredient_list = []
        rec_form = RecipeForm(user=request.user, initial={'servings': 1}) 
    else:
        data = collect_data(request)
        rec_form = RecipeForm(user=request.user, initial=data)       

    return render(request, 'recipes/create.html', {
        'rec_form': rec_form,
        'ingr_list': ingredient_list,
        'categories': categories,
        'recipes': recipes,
        'recipe': recipe,
    })


# editing a recipe
def edit_recipe(request, action):
    user_pk = request.user.pk
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)
    
    # if the action is purely numeric, only the recipe.pk was given, meaning this is the first time this view is used
    if len(action) == UUID_LEN:

        # retrieve recipe to be edited
        recipe = Recipe.objects.get(pk=action)

        # prepare ingredient_list
        if recipe.ingredients:
            ingredient_list = recipe.ingredients.split('#')
        else:
            ingredient_list = []    

        # gather data to populate form to be edited   
        data = {'title': recipe.title,
                'category': recipe.category,
                'servings': recipe.servings,
                'body': recipe.body} 
        
        # set up forms etc.
        rec_form = RecipeForm(initial=data, user=request.user)

    # handle for ingredients
    if  'add' in action or 'header' in action or 'del' in action:
        recipe = ingredient_handler(request, action)
        if isinstance(recipe, HttpResponse):
            return recipe
        else:
            ingredient_list = recipe.ingredients.split('#')
            data = collect_data(request)
            rec_form = RecipeForm(user=request.user, initial=data)
   
    # handle for RecipeForm submission
    if 'save' in action:
        if request.method == 'POST':
            form = RecipeForm(request.POST)
            if form.is_valid():
                
                recipe_pk = action.split(',')[-1]
                recipe = Recipe.objects.get(pk=recipe_pk)
                ingredient_list = recipe.ingredients.split('#')

                # check if new category was given
                new_category = request.POST.get('new_category')            
                if new_category:

                    # check if new category alredy exists
                    category_names = [cat.name for cat in categories]
                    if new_category in category_names:
                        messages.info(request, 'Category Already Exists')

                        data = collect_data(request)
                        rec_form = RecipeForm(user=request.user, initial=data)

                        return render(request, 'recipes/edit.html', {
                            'rec_form': rec_form,
                            'ingr_list': ingredient_list,
                            'categories': categories,
                            'recipes': recipes,
                            'recipe': recipe
                        })

                    # create recipe with new category       
                    recipe = edit_recipe_new_cat(request, ingredient_list, recipe)
                    recipe.save()

                    return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))
                
                # create recipe with existing category
                elif request.POST.get('category'):
                    recipe = edit_recipe_existing_cat(request, ingredient_list, recipe)
                    recipe.save()

                    return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))    

        # error message for if no category is given
            else:
                messages.info(request, 'Note: You must give a title, category and body to save the recipe')

                ingredient_list = recipe.ingredients.split('#')     
                data = collect_data(request)               
                rec_form = RecipeForm(user=request.user, initial=data)

                return render(request, 'recipes/edit.html', {
                'rec_form': rec_form,
                'recipe': recipe,
                'ingr_list': ingredient_list,
                'categories': categories,
                'recipes': recipes,
            })
            

    return render(request, 'recipes/edit.html', {
        'categories': categories,
        'recipes': recipes,
        'rec_form': rec_form,
        'ingr_list': ingredient_list,
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
        try:
            if form.is_valid():                        
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
            else:
                messages.error('Please give a category')
                return redirect('recipes:get_recipe')    
        except:
            messages.error(request, 'Oops, something went wrong. Please check that you have given a category, it is also possible that this URL does not contain a recipe')
            return redirect('recipes:get_recipe') 

    return render(request, 'recipes/get_recipe.html', {
        'form': form,
        'recipes': recipes,
        'categories': categories
    })
  
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

    # some cleanup to find incomplete recepes or empty categories and deleting them
    if recipes:
        for rec in recipes:
            if not rec.title or not rec.category or not rec.body:
                rec.delete()
                recipes = Recipe.objects.filter(user__pk=user_pk)
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
