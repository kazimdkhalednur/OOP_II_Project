from django.contrib import admin

from .models import Cart, Category, Product, ProductImage

admin.site.register(Category)
admin.site.register(Cart)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5
    max_num = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_filter = ["category", "status"]
    list_display = ["title", "discount_price", "price", "quantity"]

    class Meta:
        model = Product
