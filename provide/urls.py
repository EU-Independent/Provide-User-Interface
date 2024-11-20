from django.urls import path
from .views import provide_offer

urlpatterns = [
    path('offer/', provide_offer, name='provide_offer'),
]
