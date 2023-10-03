from django.shortcuts import render

# Create your views here.

def initMap(request):
    context = {'database_upload_field':DatabaseConfigurationForm(),
               'database_connect_button_url': reverse('database_connect_button')}
    return render(request,'mapme/map.html',context)