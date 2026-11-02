from django.shortcuts import render, get_object_or_404, redirect
import random

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Product, Warehouse, InventoryRecord
from .forms import ProductForm




def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/products.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('year')
        genre = request.POST.get('genre')
        price = request.POST.get('price')

        Product.objects.create(
            title=title, author=author, year=year, genre=genre, price=price
        )
        messages.success(request, f'Товар "{title}" успішно додано!')
        return redirect('product_list')

    return render(request, 'catalog/products_form.html')


def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Товар успішно створено!')
            return redirect('product_edit', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'catalog/product_form.html', {'form': form})


def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успішно оновлено!')
            return redirect('product_edit', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'catalog/product_form.html', {'form': form})

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Товар успішно створено!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успішно оновлено!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар успішно видалено!')
        return redirect('product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})




def inventory_list_view(request):
    records = InventoryRecord.objects.select_related('product', 'warehouse')
    return render(request, 'catalog/inventory_list.html', {'records': records})


def inventory_alerts_view(request):
    records = (
        InventoryRecord.objects
        .select_related('product', 'warehouse')
        .filter(quantity__lt=F('min_required'))
    )
    return render(request, 'catalog/inventory_alerts.html', {'records': records})


@require_POST
def inventory_replenish_view(request, count):
    products = list(Product.objects.all())
    warehouses = list(Warehouse.objects.all())
    if not products or not warehouses:
        messages.error(request, 'Спочатку створіть хоча б один товар і один склад.')
        return redirect('inventory_list')

    existing = set(InventoryRecord.objects.values_list('product_id', 'warehouse_id'))
    free_pairs = [
        (p, w) for p in products for w in warehouses
        if (p.pk, w.pk) not in existing
    ]
    random.shuffle(free_pairs)
    chosen = free_pairs[:count]

    now = timezone.now()
    with transaction.atomic():
        InventoryRecord.objects.bulk_create([
            InventoryRecord(
                product=p,
                warehouse=w,
                quantity=random.randint(1, 50),
                last_restock=now,
                min_required=random.randint(2, 10),
            )
            for p, w in chosen
        ])

    if len(chosen) < count:
        messages.warning(
            request,
            f'Додано записів: {len(chosen)} із {count} (вільних пар товар–склад більше немає).',
        )
    else:
        messages.success(request, f'Додано записів: {len(chosen)}.')
    return redirect('inventory_list')