from django.db import models
from vehicles.models import Vehicles
from user.models import CustomUser
# Create your models here.

class Reservaltion(models.Model):

    reservation_number = models.AutoField(primary_key=True)
    vehicle_id = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='reservation_list')
    owner_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='myvehicle_reservations')
    renting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='reservation_list')
    reserve_from = models.DateField(auto_now=True, auto_now_add=False)
    reserve_to = models.DateField(auto_now=False, auto_now_add=False)
    
    # renting status only set to true if the renting request is acceped by the owner user
    renting_status = models.BooleanField(default=False)


class RentelAccounts(models.Model):

    rentel_account_number = models.AutoField(primary_key=True)
    reservation_number = models.OneToOneField(Reservaltion, on_delete=models.CASCADE)
    security_deposit = models.IntegerField()
    total_rent = models.IntegerField()

    # at first the balance is the same as total rent
    balance_rent = models.IntegerField(default=total_rent)


class RentalPayments(models.Model):

    rentel_account_number = models.ForeignKey(RentelAccounts, on_delete=models.CASCADE, related_name='rent_payment_list')
    payed_amount = models.IntegerField()
    payment_date = models.DateField(auto_now=True, auto_now_add=False)

