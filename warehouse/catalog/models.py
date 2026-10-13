from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from .validators import validate_product_year

class Product(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    article = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    release_date = models.DateField(validators=[validate_product_year])

    def clean(self):
        super().clean()
        errors = {}
        if self.price is not None and self.price <= 0:
            errors['price'] = 'Ціна має бути більшою за нуль.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# class Product(models.Model):
#     title = models.CharField(max_length=255, verbose_name="Назва")
#     author = models.CharField(max_length=255, verbose_name="Автор")
#     year = models.IntegerField(verbose_name="Рік видання")
#     genre = models.CharField(max_length=100, verbose_name="Жанр")
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

#     def __str__(self):
#         return f"{self.title} ({self.author})"