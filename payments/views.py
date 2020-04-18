from django.shortcuts import render
from payments.models import PaypalPayment
from payments.serializers import PaypalPaymentSerializer
from customerdataapi.models import CustomerData
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.renderers import JSONRenderer

# Create your views here.

class PaymentPaypalView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        paypal = PaypalPayment.objects.all()
        serializer = PaypalPaymentSerializer(paypal,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaypalPaymentSerializer(data=request.data)
        myDict = dict(request.data.lists())
        if serializer.is_valid():
            instance = CustomerData.objects.filter(id=myDict.get('payer_id')[0])
            for model in instance:
                model.data['SUBSCRIPTION'] = "pepe"
                model.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)