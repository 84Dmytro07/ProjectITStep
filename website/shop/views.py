from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Category, Product
from shopping_cart.forms import CartAddProductForm

def index(request):
    return render(request, 'shop/index.html')



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


def cart(request):
    return render(request, 'shop/cart.html')

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


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/shop_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/shop_detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})
