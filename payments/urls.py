"""
URL's for Payments App Service
"""

from django.conf.urls import url, include
from payments import views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r'^', views.PaymentPaypalView.as_view()),
]