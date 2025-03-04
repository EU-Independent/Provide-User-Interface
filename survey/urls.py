from django.urls import path
from . import views


app_name = 'survey'

urlpatterns = [
    path('', views.survey_view, name='survey_view'),  # Use an empty string for the root of the survey path
]
