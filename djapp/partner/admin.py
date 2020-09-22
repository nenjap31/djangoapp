from django.contrib import admin
from .models import Partner


# Register your models here.
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address','status')
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 5


admin.site.register(Partner, PartnerAdmin)