from django.contrib import admin
from django.urls import path
from contable import views

urlpatterns = [
    path('conta', views.contable, name= "index_conta"),
]