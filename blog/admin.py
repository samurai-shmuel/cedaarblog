from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Posts, Comments, Category


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    search_fields = ('email', 'firstname', 'lastname', 'last_login', 'start_Date')
    readonly_fields = ('last_login', 'start_Date')
    list_display = ('email', 'firstname', 'lastname', 'is_staff', 'is_active', 'is_admin', 'last_login', 'start_Date')
    list_filter = ('is_staff', 'is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_admin')}
        ),
    )
    ordering = ('email','firstname', 'lastname')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Category)


# Register your models here.
