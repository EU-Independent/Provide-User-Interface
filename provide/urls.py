from django.urls import path
from .views import provide_offer, upload_view

urlpatterns = [
    path('', provide_offer, name='provide_offer'),
    path("upload/", upload_view, name="upload"),  # Handles file uploads

]
