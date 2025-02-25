from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.provide_offer, name='provide_offer'),

    path('upload/', views.upload_view, name='file_upload'),  

    path('upload/<int:file_id>/', views.upload_view, name='file_download'),  
]
