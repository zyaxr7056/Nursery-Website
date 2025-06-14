from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin  # <-- using Unfold's ModelAdmin
from unfold.contrib.import_export.forms import (ExportForm, ImportForm)
from unfold.forms import (AdminPasswordChangeForm, UserChangeForm,
                          UserCreationForm)
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter

from .models import Plant, User_details

# admin.site.register(Plant)
# admin.site.register(User_details)
# Register your models here.
admin.site.unregister(User) # Unregister the default User model to customize it

@register(User)
class UserAdmin(BaseUserAdmin,ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Plant)
class PlantAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('name', 'Category', 'price', 'Quantity', 'created_at')
    list_filter = ('Category',)
    search_fields = ('name', 'Category', 'Desciption')
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'Category', 'price', 'Quantity')
        }),
        ('Description & Media', {
            'fields': ('Desciption', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter_submit = True 
    list_filter = ['Category',
                   ("created_at", RangeDateFilter)]

@admin.register(User_details)
class UserAdmin(ModelAdmin):
    list_display = ('user_name', 'email', 'Phone_number')
    search_fields = ('user_name', 'email')

