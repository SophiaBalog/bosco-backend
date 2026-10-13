from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from .validators import validate_product_year, validate_article_prefix, MaxWords

class Product(models.Model):
    title = models.CharField(
        max_length=200, 
        validators=[MinLengthValidator(2), MaxWords(10)],
        verbose_name="Назва продукту"
    )
    article = models.CharField(
        max_length=50, 
        unique=True, 
        validators=[validate_article_prefix],
        verbose_name="Артикул"
    )
    description = models.TextField(blank=True, verbose_name="Опис")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        verbose_name="Ціна"
    )
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Ціна зі знижкою"
    )
    release_date = models.DateField(
        validators=[validate_product_year],
        verbose_name="Дата випуску"
    )

    def clean(self):
        super().clean()
        errors = {}
        
        if self.price is not None and self.price <= 0:
            errors['price'] = ('Ціна мусить бути більшою за 0.')
            
        if self.price is not None and self.discount_price is not None:
            if self.discount_price >= self.price:
                errors['discount_price'] = ('Ціна зі знижкою має бути меншою за звичайну ціну.')
                
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# class Product(models.Model):
#     title = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
#     article = models.CharField(max_length=50, unique=True)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
#     release_date = models.DateField(validators=[validate_product_year])

#     def clean(self):
#         super().clean()
#         errors = {}
#         if self.price is not None and self.price <= 0:
#             errors['price'] = 'Ціна має бути більшою за нуль.'
#         if errors:
#             raise ValidationError(errors)

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title


# class Product(models.Model):
#     title = models.CharField(max_length=255, verbose_name="Назва")
#     author = models.CharField(max_length=255, verbose_name="Автор")
#     year = models.IntegerField(verbose_name="Рік видання")
#     genre = models.CharField(max_length=100, verbose_name="Жанр")
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

#     def __str__(self):
#         return f"{self.title} ({self.author})"