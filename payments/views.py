"""
Views for payments.
"""

from payments.models import PaypalPayment
from payments.serializers import PaypalPaymentSerializer
from customerdataapi.models import CustomerData
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from datetime import datetime

# API service with get and post, where the storage of the IPN message 
# is handled and the requested change in the consumer model is generated.

class PaymentPaypalView(APIView):
    permission_classes = (permissions.AllowAny,)

    # The stored IPN messages are obtained.
    def get(self, request):
        paypal = PaypalPayment.objects.all()
        serializer = PaypalPaymentSerializer(paypal,many=True)
        return Response(serializer.data)
    
    # The IPN message models are created through the serializer,
    # and in turn the customer data is modified.
    def post(self, request):
        serializer = PaypalPaymentSerializer(data=request.data)
        ipn_data = dict(request.data.lists())
        if serializer.is_valid():
            # Obtaining the client to modify.
            instance = CustomerData.objects.filter(id=ipn_data.get('payer_id')[0])
            if ipn_data.get('payment_status')[0] == "Completed": 
                # It is verified if the payment is completed
                # and the purchased plan is obtained.
                plan = ipn_data.get('item_name')[0]
            else:
                # If the payment is not completed, the account is changed to free.
                plan = "free"
            for model in instance:
                plan_settings(model, model.data['SUBSCRIPTION'], plan)
                model.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function that manages account changes.
def plan_settings(customer, current_plan, new_plan):
    now = datetime.now()
    customer.data['LAST_PAYMENT_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    if current_plan == new_plan:
        # If the plan has not changed, the settings remain 
        # and only the payment date is updated.
        pass
    else:
        if new_plan == "free":
            # If the new plan is free, the account is degraded and the settings are reset.
            customer.data['SUBSCRIPTION'] = new_plan
            customer.data['ENABLED_FEATURES']['CERTIFICATES_INSTRUCTOR_GENERATION'] = False
            customer.data['ENABLED_FEATURES']['ENABLE_COURSEWARE_SEARCH'] = False
            customer.data['ENABLED_FEATURES']['ENABLE_EDXNOTES'] = False
            customer.data['ENABLED_FEATURES']['ENABLE_DASHBOARD_SEARCH'] = False
            customer.data['ENABLED_FEATURES']['INSTRUCTOR_BACKGROUND_TASKS'] = False
            customer.data['ENABLED_FEATURES']['ENABLE_COURSE_DISCOVERY'] = False
            if 'UPGRADE_DATE' in customer.data:
                del customer.data['UPGRADE_DATE']
            customer.data['DOWNGRADE_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif new_plan == "basic":
            # If the new plan is basic, it can happen that it is an upgrade or a downgrade
            # and it is compared with the current plan.
            if current_plan == "premium":
                customer.data['SUBSCRIPTION'] = new_plan
                if 'UPGRADE_DATE' in customer.data:
                    del customer.data['UPGRADE_DATE']
                customer.data['DOWNGRADE_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                customer.data['SUBSCRIPTION'] = new_plan
                if 'DOWNGRADE_DATE' in customer.data:
                    del customer.data['DOWNGRADE_DATE']
                customer.data['UPGRADE_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif new_plan == "premium":
            # If the new plan is premium, it can only be an upgrade.
            customer.data['SUBSCRIPTION'] = new_plan
            if 'DOWNGRADE_DATE' in customer.data:
                    del customer.data['DOWNGRADE_DATE']
            customer.data['UPGRADE_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")