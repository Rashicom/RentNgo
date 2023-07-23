# Generated by Django 4.2.3 on 2023-07-23 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicles', '0001_initial'),
        ('rental_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='owner_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='requested_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='vehicle_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicles.vehicles'),
        ),
        migrations.AddField(
            model_name='rental_reviews',
            name='commented_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rental_reviews',
            name='commenter_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rental_reviews',
            name='reservation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.reservation'),
        ),
        migrations.AddField(
            model_name='rental_payments',
            name='rent_account_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.rental_accounts'),
        ),
        migrations.AddField(
            model_name='rental_accounts',
            name='reservation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.reservation'),
        ),
        migrations.AddField(
            model_name='rental_accounts',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
