from django.contrib import admin
from django.urls import path
from contable import views

urlpatterns = [
    path('', views.contable, name= "index"),
]