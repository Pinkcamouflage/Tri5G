from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import TemplateView
from .utils.connection_utils import DatabaseUtils
from .utils.dataparser_utils import DataFormatter
from .utils.datamanagement import Factory
import pdb
from .forms import DatabaseConfigurationForm
from django.urls import reverse
import json

def initMap(request):
    context = {'database_upload_field':DatabaseConfigurationForm(),
               'database_connect_button_url': reverse('database_connect_button')}
    return render(request,'mapme/map.html',context)

def getKpiForm(request):
    if request.method == 'POST':
        data = request.Post.get('data',None)
        return HttpResponse("Data received successfully.")
    else:
        return render(request, 'your_template.html')

def initDatabaseConnection(request):

    if request.method == 'POST':
        database_type = request.POST.get('database_type')
        hostname = request.POST.get('hostname')
        port = request.POST.get('port')
        database_name = request.POST.get('database_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Hardcoded (Michael wanted this, its a direct connection to some mongodb rather than dynamic)
        connection_params = {
            'database_type': 'mongodb',
            'hostname': 'localhost',
            'port': '27017',
            'database_name': 'telekom',
            'username': username,
            'password': password,
        }

        try:
            db_connection = DatabaseUtils.establishDatabaseConnection(connection_params)
            if db_connection:
                request.session['db_connection_params'] = connection_params
                collection_info = DatabaseUtils.collectionInfo(connection_params,connection_params['database_name'])
                db_connection.close()
                return JsonResponse(collection_info, status = 200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

#whenever a user clicks the toggle button the data is then added to the users sqlite database, a userbase is a user specific database
def addData(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        collection_name = data.get('collectionName')# Collection Name is passed as a response ie the disered Collections Data will be added.
        try:
            #The Connection parameters are stored within each user session
            connection_params = request.session.get('db_connection_params')
            collection_documents = DatabaseUtils.collectionData(collection_name, connection_params)

            #This part is simply to change the id Object into a string, so that the data can be serialized as a JsonObject
            #later
            for item in collection_documents:
                if '_id' in item:
                    item['_id'] = str(item['_id'])

            geoFactory = Factory()
            geo_objects = geoFactory.produceGeoObjects(collection_documents)

            return JsonResponse({"geojson": geo_objects},status =200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return HttpResponse("Data added to the userbase successfully.")

def removeData(request):

    if request.method == 'POST':
        print()
        
def add_data_to_map(request):
    print()

def create_neuralnetwork(request):
    print()
