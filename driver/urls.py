from django.urls import path
from driver import views
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('create-driver/', views.CreateDriver.as_view()),
    path('driver-list/', views.DriverList.as_view()),
    path('retrieve-driver/<int:pk>/', views.RetrieveDriver.as_view()),
    path('update-driver/<int:pk>/', views.UpdateDriver.as_view()),
    path('delete-driver/<int:pk>/',views.DeleteDriver.as_view()),
]  + static(MEDIA_URL, document_root=MEDIA_ROOT)