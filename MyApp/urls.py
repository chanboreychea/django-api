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
from MyApp.controllers import views, category_view

urlpatterns = [
    path("", views.homepage),
    path("api/v1/categories/index", category_view.index),
    path("api/v1/categories/store", category_view.store),
    path("api/v1/categories/update/<id>", category_view.update),
    path("api/v1/categories/delete/<id>", category_view.delete),
    path("api/v1/categories/show/<id>", category_view.show),
    path('api/v1/categories/search', category_view.search)
]
