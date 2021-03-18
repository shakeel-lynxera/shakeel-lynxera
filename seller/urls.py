from django.urls import path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL
from .views import *


urlpatterns = [
    # path('register/', register),
    path('add-vendor/', add_vendor),
    path('show-vendor/', show_vendor),
    path('get-shop-seller-detais/', get_shop_seller_detais),
    path('get-shop-seller-vendor-product-detais/', get_shop_seller_vendor_product_detais_for_add_product),
    path('add-product-in-shop/', Add_Product_in_shop),
    path('get_Product_for_shop/', Get_Product_for_shop)
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
