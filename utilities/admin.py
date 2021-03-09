from django.contrib import admin
from utilities.models import LogEntryForException, Role

# Register your models here.

admin.site.register(Role)
admin.site.register(LogEntryForException)