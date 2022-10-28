from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
from geoalchemy2 import Geometry, WKTElement
from geo.Geoserver import Geoserver
import datetime

# Create your models here.
geo = Geoserver('http://127.0.0.1:8080/geoserver', username='admin', password='sushant@')

class Tiff(models.Model):
  name=models.CharField(max_length=50)
  description = models.CharField(max_length=1000,blank=True)
  file = models.FileField(upload_to='%Y/%m/%d')
  uploaded_date = models.DateField(default=datetime.date.today,blank=True)
  
  def __str__(self):
    return self.name
  
@receiver(post_save,sender=Tiff)
def  publish_data(sender,instance,created,**kwargs):
  file = instance.file.path
  file_format = os.path.basename(file).split(".")[-1];
  file_name = os.path.basename(file).split(".")[0];
  file_path = os.path.dirname(file);
  name = instance.name
  geo.create_coveragestore(file,layer_name=name, workspace='geoapp')
  geo.create_coveragestyle(file, style_name=name, workspace='geoapp', color_ramp='RdBu_r')
  geo.publish_style(layer_name=name, style_name=name, workspace='geoapp')
  
@receiver(post_delete,sender=Tiff)
def delete_data(sender,instance,**kwargs):
  geo.delete_layer(instance.name,'geoapp')