from django.urls import path
from . import views

urlpatterns = [
  path('Base/', views.Base, name='Base'),
  path('upload-images/', views.upload_images, name='upload_images')
]