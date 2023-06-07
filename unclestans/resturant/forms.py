from django import forms
from main.models import MenuItem

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'image', 'price', 'category']
