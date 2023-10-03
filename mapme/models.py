from django.db import models
import uuid
from django.contrib.auth.models import User

class Object(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    type = models.CharField(max_length=30)
    color = models.CharField(max_length=30,null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.name
    

class BaseStation(models.Model):
    object = models.ForeignKey(Object, on_delete = models.CASCADE)
    name = models.TextField(null=False,blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cell(models.Model):
    pci = models.IntegerField(null=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    basestation = models.ForeignKey(BaseStation,on_delete = models.CASCADE)

    def __str__(self):
        return self.name
    
class DatabaseConfiguration(models.Model):
    DATABASE_TYPE_CHOICES = [
        ('mongodb', 'MongoDB'),
        ('postgres', 'PostgreSQL'),
    
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    database_type = models.CharField(max_length=50, choices = DATABASE_TYPE_CHOICES, default='MongoDB')
    hostname = models.CharField(max_length=100,default='localhost')
    port = models.PositiveIntegerField(default='27017')
    database_name = models.CharField(max_length=100,default='telekom')
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def get_connection_settings(self):
        return {
            'database_type': self.database_type,
            'hostname': self.hostname,
            'port': self.port,
            'database_name': self.database_name,
            'username': self.username,
            'password': self.password,
        }
    
class JsonData(models.Model):
    data = models.JSONField()