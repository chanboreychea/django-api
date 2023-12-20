"""
URL configuration for DjRestApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from MyApp.controllers import (
    views,
    category_view,
    product_view,
    sale_view,
    sale_detail_view,
    purchase_view,
)

urlpatterns = [
    path("", views.homepage),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ------------------------------------------------------
    path("api/v1/categories/index", category_view.index),
    path("api/v1/categories/store", category_view.store),
    path("api/v1/categories/update/<id>", category_view.update),
    path("api/v1/categories/delete/<id>", category_view.delete),
    path("api/v1/categories/show/<id>", category_view.show),
    path("api/v1/categories/search", category_view.search),
    # ------------------------------------------------------
    path("api/v1/products/index", product_view.index),
    path("api/v1/products/store", product_view.store),
    path("api/v1/products/update/<id>", product_view.update),
    path("api/v1/products/delete/<id>", product_view.delete),
    path("api/v1/products/show/<id>", product_view.show),
    path("api/v1/products/search", product_view.search),
    # -------------------------------------------------------
    path("api/v1/sales/index", sale_view.index),
    path("api/v1/sales/store", sale_view.sale_commit),
    path("api/v1/sales/show/<id>", sale_view.show),
    # -------------------------------------------------------
    path("api/v1/saledetails/index", sale_detail_view.index),
    path("api/v1/saledetails/show/<id>", sale_detail_view.show),
    # -------------------------------------------------------
    path("api/v1/purchases/index", purchase_view.index),
    path("api/v1/purchases/store", purchase_view.purchase_commit),
    path("api/v1/purchases/show/<id>", purchase_view.show),
]
