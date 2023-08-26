from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import vehicle_registraion_serializer, vehicle_category_serializer,vehicle_sub_category_serializer,vehicle_company_serializer,vehicle_model_serializer, vehicles_serializer, VehicleList
from .models import Vehicle_images, Vehicles
# Create your views here.


class register_vehicle(APIView):
    
    permission_classes = [IsAuthenticated]
    serialiser_class = vehicle_registraion_serializer

    @transaction.atomic
    def post(self, request, format=None):
        """
        this method is registreting a vehicle and returns details
        we have total 6 tables to update. nested serializers could be deficult for frond end developers to make request
        in order to simplify first we are sirealizing all field using serializer set as global
        then validate with all tables and save
        """
        
        
        print("vihicle registration request hit")
        # serializing data
        serializer = self.serialiser_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("serialized")

        # serializing all the data by its models tables to check the provided constrains
        # vehicle category
        vehicle_category_srlzr = vehicle_category_serializer(data=request.data)
        vehicle_category_srlzr.is_valid(raise_exception=True)
        vehicle_category_instance,_ = vehicle_category_srlzr.save()
        print("vehicle category updated")

        # vehicle sub category
        vehicle_sub_category_srlzr = vehicle_sub_category_serializer(data=request.data)
        vehicle_sub_category_srlzr.is_valid(raise_exception=True)
        vehicle_sub_category_instance,_ = vehicle_sub_category_srlzr.save(vehicle_category_id=vehicle_category_instance)
        print("vihicle sub category added")
        
        # vehicle company
        vehicle_company_srlzr = vehicle_company_serializer(data=request.data)
        vehicle_company_srlzr.is_valid(raise_exception=True)
        vehicle_company_instance,_ = vehicle_company_srlzr.save()
        print("vehicle company updated")

        # vehicle model
        vehicle_model_srlzr = vehicle_model_serializer(data=request.data)
        vehicle_model_srlzr.is_valid(raise_exception=True)
        vehicle_model_instance,_= vehicle_model_srlzr.save(vehicle_company_id=vehicle_company_instance,vehicle_sub_category_id=vehicle_sub_category_instance)
        print("vehicle model updated")
        
        # vehicle
        vehicles_srlzr = vehicles_serializer(data=request.data)
        vehicles_srlzr.is_valid(raise_exception=True)
        vehicle_instance = vehicles_srlzr.save(user_id=request.user,vehicle_model_id=vehicle_model_instance)
        print("final vehicle updated")

        # vehicle image
        # multiple images
        images = request.FILES.getlist('image')
        for img in images:
            new_image = Vehicle_images(image=img, vehicle_id=vehicle_instance)
            new_image.save()
        return Response(serializer.data)


class GetVehicles(APIView):

    permission_classes = [AllowAny]
    serializer_class = VehicleList
    def get(self, request, format=None):
        vehicle_list = Vehicles.objects.all()
        serializer = self.serializer_class(vehicle_list, many=True)
        print(serializer.data)
        return Response(serializer.data, status=200)


