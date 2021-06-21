from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django import forms
from .models import User, Posts, Comments


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('subject', 'thumbnail','content','category')

        widget = {
            'subject': forms.TextInput(),
            'content': forms.Textarea(),
            'category': forms.SelectMultiple(),
        }

    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=80, help_text="Required. Add a valid email address")

    class Meta:
        model = User
        fields = ('email','firstname','lastname','about','password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment',)

