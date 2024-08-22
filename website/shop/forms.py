
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Subscriber
from .models import ContactMessage
from .models import BlogPost, BlogImage, Comment

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = user.email  #### Используйте email в качестве имени пользователя
        if commit:
            user.save()
        return user



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')  # Email обязательный

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'required': False}),
            'first_name': forms.TextInput(attrs={'required': False}),
            'last_name': forms.TextInput(attrs={'required': False}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'address', 'state_country', 'postal_zip', 'phone']
        widgets = {
            'country': forms.TextInput(attrs={'required': False}),
            'address': forms.TextInput(attrs={'required': False}),
            'state_country': forms.TextInput(attrs={'required': False}),
            'postal_zip': forms.TextInput(attrs={'required': False}),
            'phone': forms.TextInput(attrs={'required': False}),
        }



class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'email']

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your name',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
    }))



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True



class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

class BlogImageForm(forms.ModelForm):
    class Meta:
        model = BlogImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']