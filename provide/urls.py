from django.urls import path
from . import views

app_name = 'provide'  # This defines the namespace


urlpatterns = [
    path('', views.provide_offer, name='provide_offer'),
    path('test-access/', views.test_access_endpoint, name='test_access'),
    path('upload/', views.upload_view, name='file_upload'),
    path('upload/<int:file_id>/', views.upload_view, name='file_download'),
    # API endpoint for extracted uploaded data
    path('api/uploaded-data/<int:data_id>/', views.uploaded_data_api, name='uploaded_data_api'),
]
