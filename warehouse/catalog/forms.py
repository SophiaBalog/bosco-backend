from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'article', 'description', 'price', 'release_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'article': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'title': 'Назва продукту',
            'article': 'Артикул',
            'description': 'Опис товару',
            'price': 'Ціна (грн)',
            'release_date': 'Дата випуску',
        }
        help_texts = {
            'article': 'Введіть унікальний ідентифікатор товару.',
            'price': 'Вкажіть вартість у гривнях.',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        return title.strip().capitalize()