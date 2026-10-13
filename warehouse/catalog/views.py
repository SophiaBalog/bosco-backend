from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
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