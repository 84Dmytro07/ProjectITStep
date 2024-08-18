
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

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