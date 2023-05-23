from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Recipe, Category


class IngredientForm(forms.Form):
    ingredient = forms.CharField(widget=forms.TextInput(
        attrs={'autofocus': True}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        ingredient = cleaned_data.get('ingredient')
        if not ingredient:
            raise forms.ValidationError('Enter an ingredient')


class RecipeForm(forms.ModelForm):
    new_category = forms.CharField(required=False, label="New Category")
    cat_image = forms.URLField(required=False, label="Image", widget=forms.TextInput(
        attrs={'placeholder': 'paste link here'}))
    cat_description = forms.CharField(required=False, label="Description", widget=forms.Textarea(
        attrs={'rows': '4', 'cols': '12', 'placeholder': 'Short description of new category'}))

    class Meta:
        model = Recipe
        fields = ['category', 'title', 'body', 'servings']
        widgets = {
            'body': CKEditorWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        if not category and not new_category:
            raise forms.ValidationError(
                "Please choose a category or create a new one.")
        

class ScraperForm(forms.Form):
    url = forms.URLField(label="Recipe URL", widget=forms.TextInput(
        attrs={'placeholder': 'paste link here'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all())
    new_category = forms.CharField(required=False, label="New Category")
    cat_image = forms.URLField(required=False, label="Image", widget=forms.TextInput(
        attrs={'placeholder': 'paste link here'}))
    cat_description = forms.CharField(required=False, label="Description", widget=forms.Textarea(
        attrs={'rows': '4', 'cols': '12', 'placeholder': 'Short description of new category'}))        
