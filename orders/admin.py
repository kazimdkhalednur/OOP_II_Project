from django.contrib import admin

from .models import Order, OrderItem, Transaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "created_at"]
    list_filter = ["status"]


admin.site.register(Transaction)
admin.site.register(OrderItem)
