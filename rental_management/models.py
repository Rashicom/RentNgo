from django.db import models
from vehicles.models import Vehicles
from user.models import CustomUser

# Create your models here.



# user book for a vehicle
class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    vehicle_id = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    requested_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requested_user_id')
    owner_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owner_user_id')
    
    reserve_from = models.DateField()
    reserve_to = models.DateField()
    request_status = models.BooleanField(default=False)


# rental accoutns
class Rental_accounts(models.Model):
    rental_account_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    
    security_deposit = models.IntegerField(default=2000)
    total_rent = models.IntegerField()
    balance_rent = models.IntegerField()


# rental payments
class Rental_payments(models.Model):
    rental_payment_id = models.AutoField(primary_key=True)
    rent_account_id = models.ForeignKey(Rental_accounts, on_delete=models.CASCADE)
    
    rental_amount = models.IntegerField()
    rental_payment_date = models.DateField(auto_now_add=True)
    

# review
class Rental_reviews(models.Model):
    
    rental_reviews_id = models.AutoField(primary_key=True)
    commenter_user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='commenter_user_id')
    commented_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commented_user_id')
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    review = models.TextField()