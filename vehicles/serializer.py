from rest_framework import serializers
from .models import Vehicles, Vehicle_sub_category, Vehicle_category, Vehicle_company, Vehicle_model, Vehicle_images
from user.models import CustomUser

class vehicle_category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle_category
        fields = '__all__'
    
    # save() internally calling the create methord so we are overriding the create method
    # overridign create methord to get_or_create to avoide recreating the excisting data
    def create(self, validated_data):
        instance = Vehicle_category.objects.get_or_create(**validated_data)
        return instance


class vehicle_sub_category_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vehicle_sub_category
        fields = ['vehicle_sub_category']
    
    # save() internally calling the create methord so we are overriding the create method
    # overridign create methord to get_or_create to avoide recreating the excisting data
    def create(self, validated_data):
        instance = Vehicle_sub_category.objects.get_or_create(**validated_data)
        return instance

    

class vehicle_company_serializer(serializers.ModelSerializer):
    """
    company name is set to be unique in the models.py.
    so the seriazer check the uniqueness for the given value.
    we dont want to check when it serializing , becouse we use get_or_create method in the serializer create method
    if a value already exsist its geting instence insted of creating. so we override the checking from database 
    """
    company_name = serializers.CharField(required=True)

    class Meta:
        model = Vehicle_company
        fields = ['company_name']

    # save() internally calling the create methord so we are overriding the create method
    # overridign create methord to get_or_create to avoide recreating the excisting data
    def create(self, validated_data):
        instance = Vehicle_company.objects.get_or_create(**validated_data)
        return instance
    

class vehicle_model_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vehicle_model
        fields = ['color','vehicle_model_name']
    
    # save() internally calling the create methord so we are overriding the create method
    # overridign create methord to get_or_create to avoide recreating the excisting data
    def create(self, validated_data):
        instance = Vehicle_model.objects.get_or_create(**validated_data)
        return instance



class vehicles_serializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicles
        fields = ['vehicle_no','available_from','available_to','rent']

    
    


class vehicle_registraion_serializer(serializers.Serializer):
    vehicle_category = serializers.CharField(required=True)
    vehicle_sub_category = serializers.CharField(required=True)
    company_name = serializers.CharField(required=True)
    color = serializers.CharField(required=True)
    vehicle_model_name = serializers.CharField(required=True)
    vehicle_no = serializers.CharField(required=True)
    available_from = serializers.CharField(required=False)
    available_to = serializers.CharField(required=True)
    rent = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','contact_number','social_rank']
    
class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle_images
        fields = ['image']

class VehicleList(serializers.ModelSerializer):
    user = CustomUserSerializer(source='user_id')
    vehicle_images = VehicleImageSerializer(many=True, read_only=True, source='vehicle_images_set')
    class Meta:
        model = Vehicles
        fields = ['vehicle_id','user','vehicle_model_id','vehicle_no','available_from','available_to','is_available','rent','vehicle_images']
        depth = 2

