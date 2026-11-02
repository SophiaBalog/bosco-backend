from django import forms
from .models import Product

# warehouse/catalog/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'article', 'category', 'description', 'price', 'discount_price', 'release_date']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'article': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        return title.strip().capitalize()

    def clean_article(self):
        article = self.cleaned_data.get('article', '')
        return article.upper().strip()

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')

        if price and discount_price:
            if discount_price >= price:
                self.add_error(
                    'discount_price', 
                    _('Ціна зі знижкою не може бути більшою або рівною звичайній ціні.')
                )
        return cleaned_data


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['title', 'article', 'description', 'price', 'release_date']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'article': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'price': forms.NumberInput(attrs={'class': 'form-control'}),
#             'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#         }
#         labels = {
#             'title': 'Назва продукту',
#             'article': 'Артикул',
#             'description': 'Опис товару',
#             'price': 'Ціна (грн)',
#             'release_date': 'Дата випуску',
#         }
#         help_texts = {
#             'article': 'Введіть унікальний ідентифікатор товару.',
#             'price': 'Вкажіть вартість у гривнях.',
#         }

#     def clean_title(self):
#         title = self.cleaned_data.get('title', '')
#         return title.strip().capitalize()