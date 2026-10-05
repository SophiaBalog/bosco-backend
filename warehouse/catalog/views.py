from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

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
        return redirect('/catalog/products/')

    return render(request, 'catalog/product_form.html')