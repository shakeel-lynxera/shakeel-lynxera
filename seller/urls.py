from django.urls import path
from seller import views
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('create-seller/', views.CreateSeller.as_view()),
    path('seller-list/', views.SellerList.as_view()),
    path('retrieve-seller/<int:pk>/', views.RetrieveSeller.as_view()),
    path('update-seller/<int:pk>/', views.UpdateSeller.as_view()),
    path('delete-seller/<int:pk>/',views.DeleteSeller.as_view()),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)