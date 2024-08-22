from django.contrib import admin
from .models import Category, Product, Subscriber, ContactMessage, BlogPost, BlogImage, Comment


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




class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    inlines = [BlogImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog_post', 'created_at')
    search_fields = ('author__username', 'blog_post__title')


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
