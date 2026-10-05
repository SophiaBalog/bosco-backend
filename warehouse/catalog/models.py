from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Назва")
    author = models.CharField(max_length=255, verbose_name="Автор")
    year = models.IntegerField(verbose_name="Рік видання")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    def __str__(self):
        return f"{self.title} ({self.author})"