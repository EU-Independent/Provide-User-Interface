from django.apps import AppConfig
import requests
from django.conf import settings

class ProvideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'provide'

    def ready(self):
        self.run_registration_process()

    def run_registration_process(self):
        connector_url = getattr(settings, 'CONNECTOR_URL', None)
        broker_url = getattr(settings, 'BROKER_URL', None)
        headers = {
            'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ=',
            'Content-Type': 'application/json',
            'accept': '*/*'
        }

        # Step 1: Create a broker
        broker_payload = {
            "title": "broker registration title",
            "description": "broker registration description",
            "location": broker_url + "/broker/infrastructure/"
        }
        try:
            create_broker_url = connector_url + '/api/brokers'
            print(f"Step 1: Creating broker at {create_broker_url}")
            response = requests.post(create_broker_url, headers=headers, json=broker_payload, verify=settings.ENFORCE_CONNECTOR_SSL)
            print(f"Response Code: {response.status_code}")
            print(f"Response Message: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Step 1 failed: {e}")
            return

        # Step 2: Check broker status
        try:
            check_brokers_url = connector_url + '/api/brokers?page=0&size=30'
            print(f"Step 2: Checking broker status at {check_brokers_url}")
            response = requests.get(check_brokers_url, headers=headers, verify=settings.ENFORCE_CONNECTOR_SSL)
            print(f"Response Code: {response.status_code}")
            print(f"Response Message: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Step 2 failed: {e}")
            return

        # Step 3: Register the connector
        try:
            register_connector_url = connector_url + f'/api/ids/connector/update?recipient={broker_url}/broker/infrastructure/'
            print(f"Step 3: Registering connector at {register_connector_url}")
            response = requests.post(register_connector_url, headers=headers, data='', verify=settings.ENFORCE_CONNECTOR_SSL)
            print(f"Response Code: {response.status_code}")
            print(f"Response Message: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Step 3 failed: {e}")
            return

        # Step 4: Confirm broker registration
        try:
            print(f"Step 4: Confirming broker registration at {check_brokers_url}")
            response = requests.get(check_brokers_url, headers=headers, verify=settings.ENFORCE_CONNECTOR_SSL)
            print(f"Response Code: {response.status_code}")
            print(f"Response Message: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Step 4 failed: {e}")