from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('login_view', login_view, name='login'),
    path('cartpage', cartpage, name="cartpage"),
    path("add_to_cart/<int:pk>", add_to_cart, name="add_to_cart"),
    path("cart", cart, name="cart"),
    path("remove_from_cart/<int:pk>", remove_from_cart, name="remove_from_cart"),
    path("index", Index, name="index"),
    path("", homepage, name="homepage"),
    path('car/<int:pk>', booking_invoice, name='booking_invoice'),
    path("signout", signout, name="signout")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
