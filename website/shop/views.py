from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Category, Product
from shopping_cart.forms import CartAddProductForm
import random



def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def blog(request):
    return render(request, 'shop/blog.html')

def blog_detail(request, blog_id):
    return render(request, 'shop/blog_detail.html', {'blog_id': blog_id})

def services(request):
    return render(request, 'shop/services.html')

def terms(request):
    return render(request, 'shop/terms.html')

def disclaimer(request):
    return render(request, 'shop/disclaimer.html')

def support(request):
    return render(request, 'shop/support.html')



def checkout(request):
    return render(request, 'shop/checkout.html')

def profile(request):
    return render(request, 'shop/profile.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:index')
    else:
        form = SignUpForm()
    return render(request, 'shop/registration_user.html', {'form': form})

class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('shop:index')

#### Магазин

def product_list(request):
    products = Product.objects.all()

    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Сортировка по цене
    price_sort = request.GET.get('price_sort')
    if price_sort == 'asc':
        products = products.order_by('price')
    elif price_sort == 'desc':
        products = products.order_by('-price')

    # Фильтрация по диапазону цен
    price_range = request.GET.get('price_range')
    if price_range == 'under-500':
        products = products.filter(price__lt=500)
    elif price_range == '500-1000':
        products = products.filter(price__gte=500, price__lte=1000)
    elif price_range == 'over-1000':
        products = products.filter(price__gt=1000)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'category': Category.objects.filter(slug=category_slug).first() if category_slug else None,
        'price_sort': price_sort,
        'price_range': price_range,
    }
    return render(request, 'shop/shop_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/shop_detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})


def index(request):
    products = list(Product.objects.filter(available=True))
    random_products = random.sample(products, 3) if len(products) >= 3 else products

    context = {
        'random_products': random_products,
    }
    return render(request, 'shop/index.html', context)