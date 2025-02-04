# Generated by Django 2.2.12 on 2020-04-17 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayPalPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protection_eligibility', models.CharField(max_length=128)),
                ('address_status', models.CharField(max_length=128)),
                ('payer_id', models.CharField(max_length=128)),
                ('payment_day', models.DateField()),
                ('payment_status', models.CharField(max_length=128)),
                ('verify_sign', models.CharField(max_length=128)),
                ('receiver_id', models.CharField(max_length=128)),
                ('txn_type', models.CharField(max_length=128)),
                ('item_name', models.CharField(max_length=128)),
                ('mc_currency', models.CharField(max_length=128)),
                ('payment_gross', models.DecimalField(decimal_places=2, max_digits=6)),
                ('shipping', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
