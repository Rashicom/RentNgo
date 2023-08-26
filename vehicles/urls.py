from django.urls import path, include
from . import views


urlpatterns = [
    path('register_vehicle/', views.register_vehicle.as_view()),
    path('get_vehicles/', views.GetVehicles.as_view()),
    
]
