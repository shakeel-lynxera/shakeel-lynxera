from django.urls import path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL
from .views import *


urlpatterns = [
    # path('register/', register),
    path('add-vendor/', add_vendor)
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
