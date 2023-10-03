from django.urls import path
from home import views

urlpatterns = [
    path('entrance/',views.get_homepage)
]