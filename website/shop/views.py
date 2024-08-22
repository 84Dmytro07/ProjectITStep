from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.views import View
from .forms import SignUpForm, BlogPostForm, BlogImageForm, CommentForm, ContactForm, SubscriptionForm, UserUpdateForm, ProfileUpdateForm
from .models import Category, Product, BlogPost, BlogImage, Comment, BlogCategory
from shopping_cart.forms import CartAddProductForm
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib import messages





def about(request):
    return render(request, 'shop/about.html')


def contact_success(request):
    return render(request, 'shop/contact_success.html')


def blog(request):
    category_slug = request.GET.get('category')
    sort_by_date = request.GET.get('sort_by_date', 'desc')

    blog_posts = BlogPost.objects.all()

    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        blog_posts = blog_posts.filter(category=category)

    if sort_by_date == 'asc':
        blog_posts = blog_posts.order_by('created_at')
    else:
        blog_posts = blog_posts.order_by('-created_at')

    categories = BlogCategory.objects.all()

    return render(request, 'shop/blog.html', {
        'blog_posts': blog_posts,
        'categories': categories,
        'selected_category': category_slug,
        'sort_by_date': sort_by_date,
    })


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


@login_required
def profile(request):
    user_profile = request.user.profile
    orders = Order.objects.filter(user=request.user)  

    context = {
        'user': request.user,
        'profile': user_profile,
        'orders': orders
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

        #  экземпляр формы пароля только если данные для нее были переданы
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



def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing to our newsletter!')
            return  redirect('shop:subscribe')
    else:
        form = SubscriptionForm()

    return render(request, 'shop/subscribe.html', {'form': form})



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message!')
            return redirect('shop:contact_success')
    else:
        form = ContactForm(user=request.user)

    return render(request, 'shop/contact.html', {'form': form})




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





@login_required
def blog_create(request):
    if request.method == 'POST':
        post_form = BlogPostForm(request.POST)
        image_forms = [BlogImageForm(request.POST, request.FILES, prefix=str(x)) for x in range(0, 3)]
        if post_form.is_valid() and all([img_form.is_valid() for img_form in image_forms]):
            blog_post = post_form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            for img_form in image_forms:
                if img_form.cleaned_data:
                    image = img_form.save(commit=False)
                    image.blog_post = blog_post
                    image.save()
            return redirect('shop:blog')
    else:
        post_form = BlogPostForm()
        image_forms = [BlogImageForm(prefix=str(x)) for x in range(0, 3)]

    return render(request, 'shop/blog_create.html', {'post_form': post_form, 'image_forms': image_forms})


def blog_detail(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    comments = blog_post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog_post = blog_post
            comment.author = request.user
            comment.save()
            return redirect('shop:blog_detail', blog_id=blog_post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'shop/blog_detail.html', {
        'blog_post': blog_post,
        'comments': comments,
        'comment_form': comment_form
    })
