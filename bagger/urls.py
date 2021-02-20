from django.urls import path
from bagger import views
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('create-bagger/', views.CreateBagger.as_view()),
    path('bagger-list/', views.BaggerList.as_view()),
    path('retrieve-bagger/<int:pk>/', views.RetrieveBagger.as_view()),
    path('update-bagger/<int:pk>/', views.UpdateBagger.as_view()),
    path('delete-bagger/<int:pk>/',views.DeleteBagger.as_view()),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)