from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
# Create your views here.


class register_vehicle(APIView):

    def get(self, request):
        return HttpResponse("vehicle registration")
        