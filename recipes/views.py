from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages

from .forms import  RecipeForm, IngredientForm
from .models import Recipe, Category

INGREDIENT_LS = []

def create(request):     
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            new_category = request.POST.get('new_category')
            if new_category:
                c = Category(name = new_category)
                c.save()
                
                categories = Category.objects.all()
                title = request.POST.get('title')
                body = request.POST.get('body')
                ingr_str = ''
                for i in INGREDIENT_LS:
                    ingr_str += f'{i},'

                r = Recipe(category = c,
                            title = title,
                            body = body,
                            ingredients = ingr_str)
                r.save()

                INGREDIENT_LS.clear()
                recipes = Recipe.objects.all()

                return redirect('recipes:create')
            else:    
                category_pk = request.POST.get('category')
                category = Category.objects.get(pk=category_pk)
                title = request.POST.get('title')
                body = request.POST.get('body')
                ingr_str = ''
                for i in INGREDIENT_LS:
                    ingr_str += f'{i},'
                r = Recipe(category = category,
                            title = title,
                            body = body,
                            ingredients = ingr_str)

                r.save()
                INGREDIENT_LS.clear()
                recipes = Recipe.objects.all()

                return redirect('recipes:create')
        else:
            messages.info(request, 'Choose a category or create a new one.')
            return redirect('recipes:create')
        
    ingr_form = IngredientForm()
    rec_form = RecipeForm()
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
       
    return render(request, 'recipes/create.html', {
        'rec_form': rec_form,
        'ingr_form': ingr_form,
        'ingr_list': INGREDIENT_LS,
        'categories': categories,
        'recipes': recipes,
    })

def ingredient_handler(request, action):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = request.POST.get('ingredient')
            if 'add' in action:
                INGREDIENT_LS.append(ingredient)
            elif 'header' in action:
                INGREDIENT_LS.append(f'!{ingredient}')
        if 'del' in action:
            if INGREDIENT_LS:
                del INGREDIENT_LS[-1]    
   
    if action[-1].isnumeric():
        recipe_pk = action.split(',')[-1]
        return redirect(reverse('recipes:edit_recipe', kwargs={'pk': recipe_pk}))

    return redirect('recipes:create') 

def index(request):
    categories = Category.objects.all()
    recipes = Recipe.objects.all()

    return render(request, 'recipes/index.html', {
        'categories': categories,
        'recipes': recipes,
    })

def view_cat(request, pk):
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
    cat_recipes = Recipe.objects.filter(category__pk = pk)

    return render(request, 'recipes/view_cat.html', {
        'cat_recipes': cat_recipes,
        'categories': categories,
        'recipes': recipes,
    })

def view_recipe(request, pk):
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
    recipe = Recipe.objects.get(pk=pk)
    ingr_list = recipe.ingredients.split(',')[:-1]

    return render(request, 'recipes/view_recipe.html', {
        'recipe': recipe,
        'ingr_list': ingr_list,
        'categories': categories,
        'recipes': recipes,
    })

def edit_recipe(request, pk):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = Recipe.objects.get(pk=pk)
            new_category = request.POST.get('new_category')
            if new_category:
                c = Category(name = new_category)
                c.save()
                categories = Category.objects.all()
                recipe.category = c
                recipe.title = request.POST.get('title')
                recipe.body = request.POST.get('body')
                ingr_str = ''
                for i in INGREDIENT_LS:
                    ingr_str += f'{i},'
                recipe.ingredients = ingr_str    
                recipe.save()
                INGREDIENT_LS.clear()                
                return redirect('/')
            else:    
                category_pk = request.POST.get('category')
                category = Category.objects.get(pk=category_pk)
                recipe.category = category
                recipe.title = request.POST.get('title')
                recipe.body = request.POST.get('body')
                ingr_str = ''
                for i in INGREDIENT_LS:
                    ingr_str += f'{i},'
                recipe.ingredients = ingr_str

                recipe.save()
                INGREDIENT_LS.clear()
                return redirect('/')
        else:
            messages.info(request, 'Choose a category or create a new one.')
            return redirect(reverse('recipes:edit_recipe', kwargs={'pk': pk}))
        
    else:    

        categories = Category.objects.all()
        recipes = Recipe.objects.all()
        recipe = Recipe.objects.get(pk=pk)
        if not INGREDIENT_LS:
            for ing in recipe.ingredients.split(',')[:-1]:
                INGREDIENT_LS.append(ing)

        data = {'category': recipe.category,
                'title': recipe.title,
                'body': recipe.body,} 
        
        rec_form = RecipeForm(initial=data)
        ingr_form = IngredientForm()

        return  render(request, 'recipes/edit.html', {
            'categories': categories,
            'recipes': recipes,
            'rec_form': rec_form,
            'ingr_list': INGREDIENT_LS,
            'ingr_form': ingr_form,
            'recipe': recipe,
        })
    




        

