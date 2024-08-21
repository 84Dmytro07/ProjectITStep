from django.contrib import admin
from .models import Category, Product, Subscriber, ContactMessage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subscribed_at')
    search_fields = ('email',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email')