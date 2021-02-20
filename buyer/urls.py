from django.urls import path
from buyer import views
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('create-buyer/', views.CreateBuyer.as_view()),
    path('buyer-list/', views.BuyerList.as_view()),
    path('retrieve-buyer/<int:pk>/', views.RetrieveBuyer.as_view()),
    path('update-buyer/<int:pk>/', views.UpdateBuyer.as_view()),
    path('delete-buyer/<int:pk>/',views.DeleteBuyer.as_view()),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)