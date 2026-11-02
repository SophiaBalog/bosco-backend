import uuid as uuid_lib

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from .validators import validate_product_year, validate_article_prefix, MaxWords


class BaseTrackedModel(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        abstract = True


class Category(BaseTrackedModel):
    name = models.CharField(max_length=100, verbose_name="Назва")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="Батьківська категорія",
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def full_path(self):
        parts, node, seen = [], self, set()
        while node is not None and node.pk not in seen:  # захист від циклів
            seen.add(node.pk)
            parts.append(node.name)
            node = node.parent
        return " → ".join(reversed(parts))

    def __str__(self):
        return self.full_path()


class Warehouse(BaseTrackedModel):
    title = models.CharField(max_length=100, verbose_name="Назва складу")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адреса")
    manager_name = models.CharField(max_length=100, verbose_name="Менеджер")

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склади"

    def __str__(self):
        return self.title


class Product(BaseTrackedModel):
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
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категорія",
    )
    warehouses = models.ManyToManyField(
        Warehouse,
        through="InventoryRecord",
        related_name="products",
    )

    class Meta:
        unique_together = ("title", "category")

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


class InventoryRecord(BaseTrackedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Товар"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, verbose_name="Склад"
    )
    quantity = models.IntegerField(verbose_name="Кількість")
    last_restock = models.DateTimeField(verbose_name="Останнє поповнення")
    min_required = models.IntegerField(verbose_name="Мінімальний запас")

    class Meta:
        unique_together = ("product", "warehouse")

    def is_below_minimum(self):
        return self.quantity < self.min_required

    def __str__(self):
        return f"{self.product} @ {self.warehouse}: {self.quantity}"