from django import forms
from subspaceapp.models import Products


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description']










