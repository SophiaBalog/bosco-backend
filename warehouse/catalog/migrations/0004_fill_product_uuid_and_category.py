import uuid

from django.db import migrations


def fill_existing_products(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    Category = apps.get_model('catalog', 'Category')

    default_category = None
    for product in Product.objects.all():
        product.uuid = uuid.uuid4()
        if product.category_id is None:
            if default_category is None:
                default_category, _ = Category.objects.get_or_create(
                    name='Без категорії', parent=None
                )
            product.category = default_category
        # у міграції використовується історична модель: save() без full_clean()
        product.save(update_fields=['uuid', 'category'])


class Migration(migrations.Migration):
    """Крок 2: унікальні uuid та категорія за замовчуванням для старих товарів."""

    dependencies = [
        ('catalog', '0003_category_warehouse_product_new_fields'),
    ]

    operations = [
        migrations.RunPython(fill_existing_products, migrations.RunPython.noop),
    ]