from django.shortcuts import render, get_object_or_404, redirect
import random

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Product, Warehouse, InventoryRecord
from .forms import ProductForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView


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


# ---------- Ролі та права ----------

class RoleQuerysetMixin:
    """Уся логіка ролей в одному місці:
    менеджер (право change_any_product) бачить усе, комірник тільки своє."""

    def get_queryset(self):
        qs = Product.objects.select_related('category', 'owner')
        if self.request.user.has_perm('catalog.change_any_product'):
            return qs
        return qs.filter(owner=self.request.user)


class ProductManageListView(LoginRequiredMixin, RoleQuerysetMixin, ListView):
    template_name = 'catalog/manage_list.html'
    context_object_name = 'products'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_product'
    raise_exception = True
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('manage_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Товар успішно створено!')
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, RoleQuerysetMixin, UpdateView):
    permission_required = 'catalog.change_product'
    raise_exception = True
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('manage_list')

    def form_valid(self, form):
        messages.success(self.request, 'Товар успішно оновлено!')
        return super().form_valid(form)


@login_required
@require_POST
def product_publish_view(request, pk):
    # перевірка власного права у view
    if not request.user.has_perm('catalog.can_publish'):
        raise PermissionDenied
    product = get_object_or_404(Product, pk=pk)
    Product.objects.filter(pk=pk).update(
        is_published=not product.is_published,
        updated_at=timezone.now(),
    )
    messages.success(request, 'Статус публікації змінено.')
    return redirect('manage_list')


class ProductStatsView(PermissionRequiredMixin, TemplateView):
    permission_required = 'catalog.view_stats'
    raise_exception = True  # залогінений без права отримає 403, а не редирект на логін
    template_name = 'catalog/stats.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total'] = Product.objects.count()
        ctx['published'] = Product.objects.filter(is_published=True).count()
        ctx['by_category'] = (
            Product.objects.values('category__name').annotate(n=Count('id')).order_by('-n')
        )
        ctx['by_owner'] = (
            Product.objects.values('owner__username').annotate(n=Count('id')).order_by('-n')
        )
        ctx['low_stock'] = InventoryRecord.objects.filter(quantity__lt=F('min_required')).count()
        return ctx