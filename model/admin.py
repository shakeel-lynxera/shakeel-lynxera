from django.contrib import admin
from model.models import mUser, mUserRegistration

class mUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(mUser, mUserAdmin)
admin.site.register(mUserRegistration, mUserAdmin)