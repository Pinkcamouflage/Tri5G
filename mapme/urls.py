from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.initMap),
    path('map/',views.getKpiForm, name = 'kpi_fetch_button'),
    path('map/',views.create_neuralnetwork, name = 'file_upload_button'),
    path('mapme/map/database_connect/', views.initDatabaseConnection, name='database_connect_button'),
    path('mapme/map/database_connect/add_data',views.addData, name = 'database_menu_button'),
]