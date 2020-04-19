# -*- coding: utf-8 -*-
"""
Database models for customerdataapi.
"""

from __future__ import absolute_import, unicode_literals

"""
Serializers for a Payment Module
"""

from rest_framework import serializers
from payments.models import PaypalPayment

# Serializer for the PaypalPayment model
class PaypalPaymentSerializer(serializers.ModelSerializer):
    protection_eligibility = serializers.CharField(max_length=128)
    address_status = serializers.CharField(max_length=128)
    payer_id = serializers.CharField(max_length=128)
    payment_date = serializers.CharField(max_length=128)
    payment_status = serializers.CharField(max_length=128)
    verify_sign = serializers.CharField(max_length=128)
    receiver_id = serializers.CharField(max_length=128)
    txn_type = serializers.CharField(max_length=128)
    item_name = serializers.CharField(max_length=128)
    mc_currency = serializers.CharField(max_length=128)
    payment_gross = serializers.DecimalField(max_digits=6, decimal_places=2)
    shipping = serializers.DecimalField(max_digits=6, decimal_places=2)

    # Configuration for the serializer, indicating the base model and the fields
    class Meta:
        model = PaypalPayment
        fields = '__all__'