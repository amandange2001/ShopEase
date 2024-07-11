"""
URL configuration for ShopEase_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ShopEase_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("watchbrowse/", views.watchbrowse, name="watchbrowse"),
    path("mycart/", views.mycart, name="mycart"),
    path("loginuser/", views.loginuser, name="loginuser"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("registeruser/", views.registeruser, name="registeruser"),
    path("Gents", views.Gents, name="Gents"),
    path("Ladies", views.Ladies, name="Ladies"),
    path("Children", views.Children, name="Children"),
    path("Couple", views.Couple, name="Couple"),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path("searchproduct", views.searchproduct, name="searchproduct"),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
  
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
