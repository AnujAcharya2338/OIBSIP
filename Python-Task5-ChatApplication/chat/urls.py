from django.urls import path
from . import views

urlpatterns = [
    path("<str:room_name>/", views.room, name="room"),
    path("", views.chat_home, name="chat_home"),
    path("<str:room_name>/", views.room, name="room"),
]