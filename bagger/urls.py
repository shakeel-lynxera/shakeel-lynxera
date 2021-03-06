from django.urls import path
from bagger import views
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('user/register/', views.userRegistration.as_view()),
    path('user/login/', views.userLogin.as_view()),
    path('user/verification/', views.userVerification.as_view()),
    path('', views.UserList.as_view()),
    # path('bagger/<int:pk>/', views.RUDBagger.as_view()),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)