from django import forms

from .models import Recipe

class IngredientForm(forms.Form):
    ingredient = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        ingredient = cleaned_data.get('ingredient')
        if not ingredient:
            raise forms.ValidationError('Enter an ingredient')

class RecipeForm(forms.ModelForm):
    new_category  = forms.CharField(required=False)    
    class Meta:
        model = Recipe
        fields = ['category', 'title', 'body']

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        if not category and not new_category:
            raise forms.ValidationError("Please choose a category or create a new one.")

