from django.db import models
from user.models import CustomUser
# Create your models here.



# vehicle category
class Vehicle_category(models.Model):

    # choices
    class category_choices(models.TextChoices):
        TWO_WHEELER = "TWO_WHEELER",
        THREE_WHEELER = "THREE_WHEELER",
        FOUR_WHEELER = "FOUR_WHEELER",
        HEAVY_VEHICLE = "HEAVY_VEHICLE",

    vehicle_category_id = models.AutoField(primary_key=True)

    vehicle_category = models.CharField(max_length=50, choices=category_choices.choices)


# vehicle sub category
class Vehicle_sub_category(models.Model):
    
    # choices
    class sub_category(models.TextChoices):
        CYCLE = "CYCLE",
        BIKE = "BIKE",
        CAR = "CAR",
        VAN = "VAN",
        BUS = "BUS",
        AUTO = "AUTO",
        TRUCK = "TRUCK",
        LORRY = "LORRY",

    vehicle_sub_category_id = models.AutoField(primary_key=True)
    vehicle_category_id = models.ForeignKey(Vehicle_category, on_delete=models.CASCADE)

    vehicle_sub_category = models.CharField(max_length=30, choices=sub_category.choices)



# //////////////////////////////vehile details////////////////////////////

# vehicle company
class Vehicle_company(models.Model):
    vehicle_company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50, unique=True)


#vehicle model 
class Vehicle_model(models.Model):
    vehicle_model_id = models.AutoField(primary_key=True)
    vehicle_company_id = models.ForeignKey(Vehicle_company, on_delete=models.CASCADE)
    vehicle_sub_category_id = models.ForeignKey(Vehicle_sub_category, on_delete=models.CASCADE)

    vehicle_model_name = models.CharField(max_length=50)

class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    vehicle_model_id = models.ForeignKey(Vehicle_model, on_delete=models.CASCADE)



# vehicles
class Vehicles(models.Model):
    
    vehicle_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vehicle_sub_category_id = models.ForeignKey(Vehicle_sub_category, on_delete=models.CASCADE)
    vehicle_model_id = models.ForeignKey(Vehicle_model, on_delete=models.CASCADE)

    vehicle_no = models.CharField(max_length=50, unique=True)
    available_from = models.DateField(auto_now_add=True)
    available_to = models.DateField(auto_now_add=True)
    rent = models.IntegerField()


# vehicle_image
class Vehicle_images(models.Model):

    vehicles_image_id = models.AutoField(primary_key=True)
    vehicle_id = models.ForeignKey(Vehicles, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="vehicle_images")
