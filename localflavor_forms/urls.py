from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<str:country_code>/', views.get_address_form, name='home'),
]
