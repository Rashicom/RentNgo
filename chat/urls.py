from django.urls import path, include
from . import views


urlpatterns = [
    path('start_chat/', views.StartConversation.as_view()),
    path('get_chat/', views.GetConversations.as_view()),
    path('get_userchat/', views.UserConversation.as_view()),
    path('get_chat_history/', views.GetChatHistrory.as_view()),
    

]