from django.contrib import admin
from .models import AdvUser


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login',)
    fields = (('username', 'email'), ('first_name', 'last_name'), 'password', 'photo', 'description', ('date_joined', 'last_login'), 'groups', 'user_permissions')
    readonly_fields = ('username', 'email', 'first_name', 'last_name', 'password', 'date_joined', 'last_login')
    # fieldsets = (
    #     ('Personal info', {'fields': ('username', 'email', 'first_name', 'last_name', 'password', 'description')}),
    # )

admin.site.register(AdvUser, AdvUserAdmin)
