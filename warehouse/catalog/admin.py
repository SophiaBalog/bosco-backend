from django.contrib import admin

from .models import Category, Product, Warehouse, InventoryRecord


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'full_path')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('title', 'article')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'manager_name')


@admin.register(InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'min_required', 'last_restock')
    list_filter = ('warehouse',)