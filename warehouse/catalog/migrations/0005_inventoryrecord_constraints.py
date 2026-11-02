import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Крок 3: обмеження (unique, NOT NULL, unique_together) та InventoryRecord."""

    dependencies = [
        ('catalog', '0004_fill_product_uuid_and_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='catalog.category', verbose_name='Категорія'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('title', 'category')},
        ),
        migrations.CreateModel(
            name='InventoryRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('quantity', models.IntegerField(verbose_name='Кількість')),
                ('last_restock', models.DateTimeField(verbose_name='Останнє поповнення')),
                ('min_required', models.IntegerField(verbose_name='Мінімальний запас')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Товар')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.warehouse', verbose_name='Склад')),
            ],
            options={
                'unique_together': {('product', 'warehouse')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='warehouses',
            field=models.ManyToManyField(related_name='products', through='catalog.InventoryRecord', to='catalog.warehouse'),
        ),
    ]