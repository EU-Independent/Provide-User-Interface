from django.apps import AppConfig
import requests
from django.conf import settings

class ProvideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'provide'

    def ready(self):
        self.check_api_status()

    def check_api_status(self):
        url = getattr(settings, 'API_URL', None)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("API is up and running")
                data = response.json()
                api_status = data['api_info']['status']
                print(f"API status: {api_status}")
            else:
                print(f"API returned an error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
