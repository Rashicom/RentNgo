from rest_framework import serializers
from .models import Vehicles, CustomUser, Vehicle_sub_category, Vehicle_category, Vehicle_company, Vehicle_model

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
    class Meta:
        model = Vehicle_company
        fields = '__all__'

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



# {"vehicle_model_id":{"vehicle_company_id":{"company_name":"hero"},"vehicle_sub_category_id":{"vehicle_category_id":{"vehicle_category":"TWO_WHEELER"},"vehicle_sub_category":"BIKE"},"color":"black","vehicle_model_name":"splender"},"vehicle_no":"10/123/20012","available_to":"2023-10-10","rent":2000}
