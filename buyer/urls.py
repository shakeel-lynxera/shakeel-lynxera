from django.urls import path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL

from . import views

urlpatterns = [
    path('', views.index, name='index'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
