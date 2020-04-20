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
import requests

# API service with get and post, where the storage of the IPN message 
# is handled and the requested change in the consumer model is generated.

URL_API_CUSTOMER_DATA = "http://localhost:8010/api/v1/customerdata/"

class PaymentPaypalView(APIView):
    # The IPN message models are created through the serializer,
    # and in turn the customer data is modified.

    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = PaypalPaymentSerializer(data=request.data)
        ipn_data = dict(request.data.lists())
        if serializer.is_valid():
            # Obtaining the client to modify.
            customer = URL_API_CUSTOMER_DATA + ipn_data.get('payer_id')[0] + '/'
            instance = requests.get(customer)
            instance_json = instance.json()
            #print(type(instance_json['data']['ENABLED_FEATURES']))
            if ipn_data.get('payment_status')[0] == "Completed": 
                # It is verified if the payment is completed
                # and the purchased plan is obtained.
                plan = ipn_data.get('item_name')[0]
            else:
                # If the payment is not completed, the account is changed to free.
                plan = "free" 
            plan_settings(instance_json['data'], instance_json['data']['SUBSCRIPTION'], plan)
            string_data = str(instance_json['data'])
            dict_json = { 'id': instance_json['id'], 'data' : string_data }
            requests.put(customer, dict_json)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function that manages account changes.
def plan_settings(customer, current_plan, new_plan):
    now = datetime.now()
    customer['LAST_PAYMENT_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    if current_plan == new_plan:
        # If the plan has not changed, the settings remain 
        # and only the payment date is updated.
        pass
    else:
        if new_plan == "free":
            # If the new plan is free, the account is degraded and the settings are reset.
            customer['SUBSCRIPTION'] = new_plan
            customer['ENABLED_FEATURES']['CERTIFICATES_INSTRUCTOR_GENERATION'] = False
            customer['ENABLED_FEATURES']['ENABLE_COURSEWARE_SEARCH'] = False
            customer['ENABLED_FEATURES']['ENABLE_EDXNOTES'] = False
            customer['ENABLED_FEATURES']['ENABLE_DASHBOARD_SEARCH'] = False
            customer['ENABLED_FEATURES']['INSTRUCTOR_BACKGROUND_TASKS'] = False
            customer['ENABLED_FEATURES']['ENABLE_COURSE_DISCOVERY'] = False
            if 'UPGRADE_DATE' in customer:
                del customer['UPGRADE_DATE']
            customer['DOWNGRADE_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif new_plan == "basic":
            # If the new plan is basic, it can happen that it is an upgrade or a downgrade
            # and it is compared with the current plan.
            if current_plan == "premium":
                customer['SUBSCRIPTION'] = new_plan
                if 'UPGRADE_DATE' in customer:
                    del customer['UPGRADE_DATE']
                customer['DOWNGRADE_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                customer['SUBSCRIPTION'] = new_plan
                if 'DOWNGRADE_DATE' in customer:
                    del customer['DOWNGRADE_DATE']
                customer['UPGRADE_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif new_plan == "premium":
            # If the new plan is premium, it can only be an upgrade.
            customer['SUBSCRIPTION'] = new_plan
            if 'DOWNGRADE_DATE' in customer:
                    del customer['DOWNGRADE_DATE']
            customer['UPGRADE_DATE'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")