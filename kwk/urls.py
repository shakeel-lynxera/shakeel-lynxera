#kwk URL Configuration
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bagger/', include('bagger.urls')),
    path('buyer/', include('buyer.urls')),
    path('driver/', include('driver.urls')),
    path('seller/', include('seller.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
