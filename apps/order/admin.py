# from django.apps import apps
from django.contrib import admin
from .models import Order, OrderItem

# app_models = apps.get_app_config('order').get_models()
# admin.site.register(list(app_models))


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(OrderItem)
