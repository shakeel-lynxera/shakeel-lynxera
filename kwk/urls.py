from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('driver/', include('driver.urls')),
    path('buyer/', include('buyer.urls')),
    path('seller/', include('seller.urls')),
    path('bagger/', include('bagger.urls')),
    path('superadmin/', admin.site.urls),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
