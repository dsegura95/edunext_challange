from django.db import models

# Create your models here.

class PaypalPayment(models.Model):
    protection_eligibility = models.CharField(max_length=128)
    address_status = models.CharField(max_length=128)
    payer_id = models.CharField(max_length=128)
    payment_date = models.CharField(max_length=128)
    payment_status = models.CharField(max_length=128)
    verify_sign = models.CharField(max_length=128)
    receiver_id = models.CharField(max_length=128)
    txn_type = models.CharField(max_length=128)
    item_name = models.CharField(max_length=128)
    mc_currency = models.CharField(max_length=128)
    payment_gross = models.DecimalField(max_digits=6, decimal_places=2)
    shipping = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "Payment with id <{}>".format(self.id)