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

    user_pk = request.user.pk  
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

                    data = collect_data(request)
                    rec_form = RecipeForm(user=request.user, initial=data)

                    return render(request, 'recipes/create.html', {
                        'rec_form': rec_form,
                        'categories': categories,
                        'recipes': recipes,
                        'recipe': recipe
                    })

                # create recipe with new category       
                recipe = create_recipe_new_cat(user_pk, request)
                recipe.save()

                return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))
            
            # create recipe with existing category
            elif request.POST.get('category'):
                recipe = create_recipe_existing_cat(user_pk, request)
                recipe.save()

                return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))    

        # error message for incomplete recipe
        else:
            messages.info(request, 'Note: You must provide a title, category and body to save the recipe')         
                
            data = collect_data(request)               
            rec_form = RecipeForm(user=request.user, initial=data)

            if not action.split(',')[-1]:
                recipe = ''

            return render(request, 'recipes/create.html', {
            'rec_form': rec_form,
            'recipe': recipe,
            'categories': categories,
            'recipes': recipes,
        })

    if action == 'new':
        recipe = ''
        rec_form = RecipeForm(user=request.user, initial={'servings': 1}) 
    else:
        data = collect_data(request)
        rec_form = RecipeForm(user=request.user, initial=data)       

    return render(request, 'recipes/create.html', {
        'rec_form': rec_form,
        'categories': categories,
        'recipes': recipes,
        'recipe': recipe,
    })

# editing a recipe
def edit_recipe(request, action):
    user_pk = request.user.pk
    recipes = Recipe.objects.filter(user__pk=user_pk)
    categories = Category.objects.filter(user__pk=user_pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():   
        
            # handle for RecipeForm submission
            if 'save' in action:
                recipe_pk = action.split(',')[-1]
                recipe = Recipe.objects.get(pk=recipe_pk)

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
                        'servings': request.POST.get('servings'),
                        'ingredients': request.POST.get('ingredients') }
                        rec_form = RecipeForm(user=request.user, initial=data)

                        return render(request, 'recipes/edit.html', {
                            'rec_form': rec_form,
                            'categories': categories,
                            'recipes': recipes,
                            'recipe': recipe
                        })

                    # edit recipe with new category       
                    recipe = edit_recipe_new_cat(request, recipe)
                    recipe.save()

                    return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))
                
                # edit recipe with existing category
                elif request.POST.get('category'):
                    recipe = edit_recipe_existing_cat(request, recipe)
                    recipe.save()

                    return redirect(reverse('recipes:view_recipe', kwargs={'rec_pk': recipe.pk}))    

            # error message for incomplete form
        else:
            messages.info(request, 'Note: You must give a title, category and body to save the recipe') 

            data = {'category': request.POST.get('category'),
            'title': request.POST.get('title'),
            'body': request.POST.get('body'),
            'servings': request.POST.get('servings'),
            'ingredients': request.POST.get('ingredients') }

            rec_form = RecipeForm(user=request.user, initial=data)

            return render(request, 'recipes/edit.html', {
            'rec_form': rec_form,
            'recipe': recipe,
            'categories': categories,
            'recipes': recipes,
        })

    

    # retrieve recipe to be edited
    recipe = Recipe.objects.get(pk=action)

    # gather data to populate form to be edited   
    data = {'title': recipe.title,
            'category': recipe.category,
            'servings': recipe.servings,
            'body': recipe.body,
            'ingredients': recipe.ingredients} 
    
    # set up forms etc.
    rec_form = RecipeForm(initial=data, user=request.user)        
            
    return render(request, 'recipes/edit.html', {
        'categories': categories,
        'recipes': recipes,
        'rec_form': rec_form,
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
