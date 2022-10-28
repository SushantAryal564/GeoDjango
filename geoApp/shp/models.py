from distutils.command.upload import upload
from unittest.util import _MAX_LENGTH
from django.db import models
import datetime
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
from geoalchemy2 import Geometry, WKTElement
from geo.Postgres import Db
from geo.Geoserver import Geoserver

db = Db(dbname="geoapp",user="postgres",password="admin",host="localhost",port="5432");
geo = Geoserver('http://127.0.0.1:8080/geoserver', username='admin', password='sushant@')

#The shapefile model
# Create your models here.
class Shp(models.Model):
  name=models.CharField(max_length=50)
  description = models.CharField(max_length=1000,blank=True)
  file = models.FileField(upload_to='%Y/%m/%d')
  uploaded_date = models.DateField(default=datetime.date.today,blank=True)
  
  def __str__(self):
    return self.name
  
  
@receiver(post_save,sender=Shp)
def  publish_data(sender,instance,created,**kwargs):
  file = instance.file.path
  file_format = os.path.basename(file).split(".")[-1];
  file_name = os.path.basename(file).split(".")[0];
  file_path = os.path.dirname(file);
  name = instance.name
  conn_str = 'postgresql://postgres:admin@localhost:5432/geoapp'
  #extract zipfile
  with zipfile.ZipFile(file,"r") as zip_ref:
    zip_ref.extractall(file_path);
  
  os.remove(file);
  
  shp = glob.glob(r'{}/**/*.shp'.format(file_path),recursive=true)[0];
  # to get shp
  gdf = gpd.read_file(shp) #make geodataframe 
  crs_name = str(gdf.crs.srs)
  epsg=4326
  # epsg = int(crs_name.replace('epsg:',''))  
  # if epsg is None:
  #   epsg = 4326 #wgs 84 coordinate system
  
  geom_type = gdf.geom_type[1]
  engine = create_engine(conn_str) # create the sqlAlchemy engine to use
  gdf['geom'] = gdf['geometry'].apply(lambda x:WKTElement(x.wkt,srid=epsg))
  gdf.drop('geometry',1, inplace=True) # drop the geometry colum since we already backup this colum with geom
  
  gdf.to_sql(name,engine,'data',if_exists='replace',index=False,dtype={'geom':Geometry('Geometry',srid=epsg)}) # post gdf to postgresql
  os.remove(shp);
  # '''
  # Publish shp to geoserver using rest
  # ''' 
  geo.create_featurestore(store_name='geoApp', workspace='geoapp', db='geoapp', host='localhost', pg_user='postgres', pg_password='admin',schema='data')
  geo.publish_featurestore(workspace='geoapp', store_name='geoApp', pg_table=name)
  
@receiver(post_delete,sender=Shp)
def delete_data(sender,instance,**kwargs):
  db.delete_table(table_name=instance.name,schema='data',dbname='geoapp')
  geo.delete_layer(instance.name,'geoapp')
