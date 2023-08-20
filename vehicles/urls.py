from django.urls import path, include
from . import views


urlpatterns = [
    path('register_vehicle/', views.register_vehicle.as_view()),
    
    
]
