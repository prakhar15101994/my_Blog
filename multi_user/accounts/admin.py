from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import MyUser, Blog
class UserAdmin(BaseUserAdmin):
   
    list_display = ('username', 'email', 'first_name', 'patient', 'doctor', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name', 'email', 'address', 'city','pincode', 'state')}),
        ('Permissions', {'fields': ('is_admin','is_active','patient', 'doctor')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',),
        }),
    )
    search_fields = ('email','username')
    ordering = ('username',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)

admin.site.register(Blog)

