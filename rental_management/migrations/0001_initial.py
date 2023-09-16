# Generated by Django 4.2.3 on 2023-09-16 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rental_accounts',
            fields=[
                ('rental_account_id', models.AutoField(primary_key=True, serialize=False)),
                ('security_deposit', models.IntegerField(default=2000)),
                ('total_rent', models.IntegerField()),
                ('balance_rent', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rental_payments',
            fields=[
                ('rental_payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('rental_amount', models.IntegerField()),
                ('rental_payment_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rental_reviews',
            fields=[
                ('rental_reviews_id', models.AutoField(primary_key=True, serialize=False)),
                ('review', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.AutoField(primary_key=True, serialize=False)),
                ('reserve_from', models.DateField()),
                ('reserve_to', models.DateField()),
                ('request_status', models.BooleanField(default=False)),
            ],
        ),
    ]
