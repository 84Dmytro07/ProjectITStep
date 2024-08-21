from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .views import MyLogoutView

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('services/', views.services, name='services'),
    path('terms/', views.terms, name='terms'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('support/', views.support, name='support'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('shop/', views.product_list, name='product_list'),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
]





