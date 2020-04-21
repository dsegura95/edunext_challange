"""
Tests for PaypalPayment API
"""
from django.test import TestCase, Client

HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

class TestViews(TestCase):
    def test_post_1(self):  
        # Test that verifies if the payment_status is not Completed, 
        # the account is changed to 'free'
        data = {
        'protection_eligibility': 'Eligible',
        'address_status': 'confirmed',
        'payer_id': '1b2f7b83-7b4d-441d-a210-afaa970e5b76',
        'payment_date': '20:12:59 Jan 13, 2009 PST',
        'payment_status': 'Failed',
        'notify_version': '2.6',
        'verify_sign': 'AtkOfCXbDm2hu0ZELryHFjY-Vb7PAUvS6nMXgysbElEn9v-1XcmSoGtf',
        'receiver_id': 'S8XGHLYDW9T3S',
        'txn_type': 'express_checkout',
        'item_name': 'basic',
        'mc_currency': 'USD',
        'payment_gross': '10.19',
        'shipping': '0.0'
        }
        response = self.client.post('http://localhost:8000/payments/paypal/', headers=HEADERS, data=data)
        self.assertEquals(response.status_code, 202)
    
    def test_post_2(self):    
        data = {
        # Test that verifies a customer's account change to premium
        'protection_eligibility': 'Eligible',
        'address_status': 'confirmed',
        'payer_id': '49a6307e-c261-414d-86f5-c6004bcec8ab',
        'payment_date': '20:12:59 Jan 13, 2009 PST',
        'payment_status': 'Completed',
        'notify_version': '2.6',
        'verify_sign': 'BtkOfCXbDm2hu0ZELryHFjY-Vb7PAUvS6nMXgysbElEn9v-1XcmSoGtf',
        'receiver_id': 'S8XGHLYDW9T3S',
        'txn_type': 'express_checkout',
        'item_name': 'premium',
        'mc_currency': 'USD',
        'payment_gross': '15.56',
        'shipping': '6.65'
        }
        response = self.client.post('http://localhost:8000/payments/paypal/', headers=HEADERS, data=data)
        self.assertEquals(response.status_code, 202)
    
    def test_post_3(self):    
        data = {
        # The same previous test, but as it is the same, only the 
        # change of the last payment day will be verified
        'protection_eligibility': 'Eligible',
        'address_status': 'confirmed',
        'payer_id': '49a6307e-c261-414d-86f5-c6004bcec8ab',
        'payment_date': '20:12:59 Jan 13, 2009 PST',
        'payment_status': 'Completed',
        'notify_version': '2.6',
        'verify_sign': 'BtkOfCXbDm2hu0ZELryHFjY-Vb7PAUvS6nMXgysbElEn9v-1XcmSoGtf',
        'receiver_id': 'S8XGHLYDW9T3S',
        'txn_type': 'express_checkout',
        'item_name': 'premium',
        'mc_currency': 'USD',
        'payment_gross': '15.56',
        'shipping': '6.65'
        }
        response = self.client.post('http://localhost:8000/payments/paypal/', headers=HEADERS, data=data)
        self.assertEquals(response.status_code, 202)
    
    def test_post_4(self): 
        # Verify a bad request because the data being sent does not
        # have the shipping field
        data = {
        'protection_eligibility': 'Eligible',
        'address_status': 'confirmed',
        'payer_id': 'a237ed14-88fb-45f3-b9b1-471877dbdc60',
        'payment_date': '20:12:59 Jan 13, 2009 PST',
        'payment_status': 'Completed',
        'notify_version': '2.6',
        'verify_sign': 'BtkOfCXbDm2hu0ZELryHFjY-Vb7PAUvS6nMXgysbElEn9v-1XcmSoGtf',
        'receiver_id': 'S8XGHLYDW9T3S',
        'txn_type': 'express_checkout',
        'item_name': 'basic',
        'mc_currency': 'USD',
        'payment_gross': '9.56',
        }
        response = self.client.post('http://localhost:8000/payments/paypal/', headers=HEADERS, data=data)
        self.assertEquals(response.status_code, 400)

    def test_post_5(self): 
        # Test that verifies a customer's account change to basic
        data = {
        'protection_eligibility': 'Eligible',
        'address_status': 'confirmed',
        'payer_id': 'a237ed14-88fb-45f3-b9b1-471877dbdc60',
        'payment_date': '20:12:59 Jan 13, 2009 PST',
        'payment_status': 'Completed',
        'notify_version': '2.6',
        'verify_sign': 'BtkOfCXbDm2hu0ZELryHFjY-Vb7PAUvS6nMXgysbElEn9v-1XcmSoGtf',
        'receiver_id': 'S8XGHLYDW9T3S',
        'txn_type': 'express_checkout',
        'item_name': 'basic',
        'mc_currency': 'USD',
        'payment_gross': '9.56',
        'shipping': '2.11'
        }
        response = self.client.post('http://localhost:8000/payments/paypal/', headers=HEADERS, data=data)
        self.assertEquals(response.status_code, 202)