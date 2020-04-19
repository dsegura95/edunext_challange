"""
Admin
"""
from django.contrib import admin
from payments.models import PaypalPayment

admin.site.register(PaypalPayment)