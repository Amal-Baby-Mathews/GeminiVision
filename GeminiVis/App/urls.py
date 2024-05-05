from django.urls import path
from . import views

urlpatterns = [
  path('Base/', views.Base, name='Base'),
  path('upload-images/', views.upload_images, name='upload_images'),
  path('show-products/', views.show_products, name='show_products'),
]