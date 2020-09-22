from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Profile'

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        if obj:  # editing an existing object
            return self.readonly_fields + ('partner',)
        return self.readonly_fields


class CustomUserAdmin(UserAdmin):
    inlines = (AccountInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_partner')
    list_select_related = ('account',)

    def get_partner(self, instance):
        return instance.account.partner

    get_partner.short_description = 'Partner'

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        current_user = request.user
        entry = Account.objects.get(user_id=current_user.id)
        partner = Account.objects.values_list('user_id').filter(partner_id=entry.partner_id)
        return qs.filter(id__in=partner)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        if obj:  # editing an existing object
            return self.readonly_fields + ('user_permissions','is_superuser')
        return self.readonly_fields


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
