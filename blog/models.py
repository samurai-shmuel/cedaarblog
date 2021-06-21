from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, about, password, **other_fields):
        if not email:
            raise ValueError(_('Email address is mandatory for a user'))

        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, about=about, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, firstname, lastname, about, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email, firstname, lastname, about, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    about = models.CharField(max_length=200, default='')
    start_Date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    email = models.EmailField(_('email_address'), unique=True, max_length=255)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'about', 'lastname']

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Category(models.Model):
    name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_absolut_url(self):
        return reverse('index')


class Posts(models.Model):
    subject = models.CharField(max_length=200)
    thumbnail = models.URLField(null=True, blank=True)
    content = RichTextField()
    category = models.ManyToManyField(Category, related_name='related_posts', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    author_str = models.CharField(max_length=150, default='Anonymous')
    likes = models.ManyToManyField(User, related_name='blogpost', blank=True)

    def __str__(self):
        return f"{self.subject}"

    def total_likes(self):
        return self.likes

    def get_absolute_url(self):
        return reverse('posts')


class Comments(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    commenter_str = models.CharField(max_length=2000, default="Anonymous")
    viewable = models.BooleanField(default=False)
    post = models.ForeignKey(Posts, related_name="comments", on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} | {self.commenter_str}"
