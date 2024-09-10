from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("<str:roomN_pk>/<str:userN_pk>/", views.room, name="room"),
]