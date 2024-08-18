from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.views import View
from .forms import SignUpForm
from .models import Category, Product
from shopping_cart.forms import CartAddProductForm
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm


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
    context = {
        'user': request.user,
    }
    return render(request, 'shop/profile.html', context)


from .models import Profile

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('shop:profile')
    else:
        form = SignUpForm()
    return render(request, 'shop/registration_user.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        # Создаем экземпляр формы пароля только если данные для нее были переданы
        password_form = PasswordChangeForm(request.user, request.POST) if request.POST.get('old_password') else None

        # Проверка всех форм
        forms_are_valid = user_form.is_valid() and profile_form.is_valid() and (
                    password_form is None or password_form.is_valid())

        if forms_are_valid:
            user_form.save()
            profile_form.save()

            if password_form:
                user = password_form.save()  # Сохраняем новый пароль
                update_session_auth_hash(request, user)  # Обновляем сессию пользователя, чтобы не разлогинивать

            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('shop:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }

    return render(request, 'shop/update_profile.html', context)



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
