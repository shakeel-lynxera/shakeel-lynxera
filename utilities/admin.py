from django.contrib import admin
from utilities.models import *

# Register your models here.

class TempProductBarcodeScannerAttributes(admin.ModelAdmin):
    list_display = ('id','barcode', 'title', 'product_img', 'category', 'type')

admin.site.register(Role)
admin.site.register(LogEntryForException)
admin.site.register(Temp_Product_Barcode_Scanner, TempProductBarcodeScannerAttributes)