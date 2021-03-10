from django.urls import path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL
from .views import *


urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('register-buyer/', register_buyer),
    path('send-verification-code-for-reset-password/', send_verification_code_for_reset_password),
    path('validate-verification-code/', validate_verification_code_for_reset_password),
    path('reset-password/', reset_password,),
    path('register-driver/',register_driver),
    path('register-seller/', register_seller),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
