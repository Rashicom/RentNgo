from django.urls import path, include
from . import views


urlpatterns = [
    path('register_vehicle/', views.register_vehicle.as_view()),
    path('get_vehicles/', views.GetVehicles.as_view()),
    path('get_available_vehicles/', views.GetAvailableVehicles.as_view()),
    path('get_user_vehicles/', views.GetUserVehicles.as_view()),
]
