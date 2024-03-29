from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Recipe, Category


class RecipeForm(forms.ModelForm):

    # custom form fields
    ingredients = forms.CharField(widget=CKEditorWidget(config_name='ingredients'), required=False)
    new_category = forms.CharField(required=False, label="New Category", widget=forms.TextInput(
        attrs={'placeholder': 'title'}))
    cat_image = forms.URLField(required=False, label="Image", widget=forms.TextInput(
        attrs={'placeholder': 'paste link here'}))
    cat_description = forms.CharField(required=False, label="Description", widget=forms.Textarea(
        attrs={'rows': '4', 'cols': '12', 'placeholder': 'Short description of category'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all())

    # ModelForm fields               
    class Meta:
        model = Recipe
        fields = ['title', 'body', 'servings']
        widgets = {
            'body': CKEditorWidget(),
        }

    # relating available categories in drop-down to specific user
    def __init__(self, *args, user=None ,**kwargs):
        super().__init__(*args, **kwargs)
        if user:
            category = self.fields['category']
            category.queryset = Category.objects.filter(user__pk=user.pk)    

    # custom form validation
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        title = cleaned_data.get('title')
        if not category and not new_category:
            raise forms.ValidationError(
                "No category given")
        if not title:
            raise forms.ValidationError(
                "No title given")


class ScraperForm(forms.Form):

    # custom form fields
    url = forms.URLField(label="Recipe URL", widget=forms.TextInput(
        attrs={'placeholder': 'paste link here'}))
    new_category = forms.CharField(required=False, label="New Category", widget=forms.TextInput(
        attrs={'placeholder': 'title'}))
    cat_image = forms.URLField(required=False, label="Image", widget=forms.TextInput(
        attrs={'placeholder': 'paste link here'}))
    cat_description = forms.CharField(required=False, label="Description", widget=forms.Textarea(
        attrs={'rows': '4', 'cols': '12', 'placeholder': 'Short description of new category'}))        
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all())

    # relating available categories in drop-down to specific user
    def __init__(self, *args, user=None ,**kwargs):
        super().__init__(*args, **kwargs)
        if user:
            category = self.fields['category']
            category.queryset = Category.objects.filter(user__pk=user.pk)

    # custom form validation
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        if not category and not new_category:
            raise forms.ValidationError(
                "No category")        