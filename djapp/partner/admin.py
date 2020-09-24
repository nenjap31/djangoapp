from django.contrib import admin
from .models import Partner
from account.models import Account


# Register your models here.
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address','status')
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 5

    def get_queryset(self, request):
        qs = super(PartnerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        current_user = request.user
        partner = Account.objects.get(user_id=current_user.id)
        return qs.filter(id=partner.partner_id)


admin.site.register(Partner, PartnerAdmin)