from django.contrib import admin
from seller.models import seller

# Register your models here.


class sellerAdmin(admin.ModelAdmin):
    pass


admin.site.register(seller, sellerAdmin)
