from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .forms import UploadMetadataForm
from .connector import runner
from .models import License, UploadedFile
import base64
from django.shortcuts import render

def provide_offer(request):
    fixed_policy_rule = (
        '{\n'
        '    "@context": {\n'
        '        "ids": "https://w3id.org/idsa/core/",\n'
        '        "idsc": "https://w3id.org/idsa/code/"\n'
        '    },\n'
        '    "@type": "ids:Permission",\n'
        '    "@id": "https://w3id.org/idsa/autogen/permission/cf1cb758-b96d-4486-b0a7-f3ac0e289588",\n'
        '    "ids:action": [\n'
        '        {\n'
        '            "@id": "idsc:USE"\n'
        '        }\n'
        '    ],\n'
        '    "ids:description": [\n'
        '        {\n'
        '            "@value": "provide-access",\n'
        '            "@type": "http://www.w3.org/2001/XMLSchema#string"\n'
        '        }\n'
        '    ],\n'
        '    "ids:title": [\n'
        '        {\n'
        '            "@value": "Example Usage Policy",\n'
        '            "@type": "http://www.w3.org/2001/XMLSchema#string"\n'
        '        }\n'
        '    ]\n'
        '}'
    )

    incident_id = request.GET.get('incident_id')
    print("Incident ID: ", incident_id)
    incident_data = {}
    metadata_data = {}

    connector_url = settings.CONNECTOR_URL
    consumer_service_url = settings.DATA_SPACE_CONSUMER_SERVICE_URL
    data_upload_service_url = settings.DATA_UPLOAD_SERVICE_URL
    access_policy_generator_url = settings.ACCESS_POLICY_GENERATOR_URL

    # Fetch Incident and Metadata Data from a single endpoint
    if incident_id:
        try:
            incident_url = f"{settings.data_upload_service_url.rstrip('/')}/incident-json/{incident_id}/"
            response = requests.get(incident_url, verify=settings.ENFORCE_CONNECTOR_SSL)
            response.raise_for_status()
            data = response.json().get('data', {})
            incident_data = data.get('incident', {})
            metadata_data = data.get('metadata', {})

        except requests.RequestException as e:
            messages.error(request, f"Failed to load data for incident {incident_id}: {e}")

    # Prepopulate the form with fetched data
    initial_data = {
        'offer_title': metadata_data.get('offer_title', ''),
        'offer_description': metadata_data.get('offer_description', ''),
        'keywords': metadata_data.get('keywords', ''),
        'offer_publisher': metadata_data.get('publisher', ''),
        'offer_language': metadata_data.get('language', ''),
        'offer_license': metadata_data.get('license', ''),
        'accessUrl': incident_data.get('accessUrl', ''),
    }

    licenses = License.objects.all()
    license_choices = [(license.name, license.name) for license in licenses]
    print("License Choices: ", license_choices)

    if request.method == 'POST':
        form = UploadMetadataForm(request.POST, license_choices=license_choices)
        if form.is_valid():
            data = form.cleaned_data

            selected_license_name = data.get('offer_license')
            selected_license = License.objects.filter(name=selected_license_name).first()
            license_url = selected_license.access_url if selected_license else ""

            user_metadata = {
                'catalog': {
                    'title': data.get('catalog_title', 'Not set'),
                    'description': data.get('catalog_description', 'Not set'),
                },
                'representation': {
                    'title': data.get('representation_title', 'Not set'),
                    'description': data.get('representation_description', 'Not set'),
                    'language': data.get('language', 'Not set'),
                    'mediaType': 'text/html',
                },
                'offer': {
                    'title': data.get('offer_title'),
                    'description': data.get('offer_description'),
                    'keywords': data.get('keywords'),
                    'paymentMethod': 'undefined',
                    'publisher': data.get('offer_publisher'),
                    'language': data.get('offer_language'),
                    'license': license_url,
                },
                'contract': {
                    'title': data.get('contract_title', 'Not set'),
                    'description': data.get('contract_description', 'Not set'),
                    'start': data.get('start'),
                    'end': data.get('end')
                },
                'rule': {
                    'title': data.get('rule_title', 'Not set'),
                    'description': data.get('rule_description', 'Not set'),
                    'value': data.get('value')
                },
                'artifact': {
                    'title': data.get('artifact_title', 'Not set'),
                    'description': data.get('artifact_description', 'Not set'),
                    'accessUrl': data.get('accessUrl', 'Not set'),
                    'automatedDownload': data.get('automatedDownload', False),
                }
            }
            print("User Metadata: ", user_metadata)

            # Send user metadata to the runner
            result = runner(user_metadata)
            if result:
                messages.success(request, "The offer was successfully provided to the data space.")
            else:
                messages.error(request, "Something went wrong with providing the offer.")

            return redirect('provide_offer')

        else:
            messages.error(request, "Form is invalid. Please correct the errors and try again.")
    else:
        form = UploadMetadataForm(request.POST or None, license_choices=license_choices)

    return render(request, 'provide/provide_offer.html', {
        'form': form,
        'licenses': licenses,
        'fixed_policy_rule': fixed_policy_rule,
        'incident_id': incident_id,
        'incidents_url': settings.DATA_UPLOAD_SERVICE_URL.rstrip('/'),
        'data_space_connector_url': connector_url,
        'data_upload_service_url': data_upload_service_url,
        'data_space_consumer_service_url': consumer_service_url,
        'access_policy_generator_url': access_policy_generator_url
    })

import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile  

@csrf_exempt
def upload_view(request, file_id=None):
    print("File upload request received.")
    
    if request.method == "POST":
        if request.FILES.get("file"):
            uploaded_file = request.FILES["file"]
            print("--------------------")
            print("uploaded_file", uploaded_file)
            print("--------------------")
            
            
            allowed_types = ["application/json"]
            if uploaded_file.content_type not in allowed_types:
                return JsonResponse({"error": "Invalid file type. Only JSON files are allowed."}, status=400)
            
            
            upload_dir = 'uploads'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)  

            
            file_instance = UploadedFile.objects.create(
                file=uploaded_file,  
                file_name=uploaded_file.name  
            )

            # Generate a unique URL for the uploaded file
            file_url = f"{settings.DOMAIN_URL}{settings.MEDIA_URL}{file_instance.file.name}"
            

            return JsonResponse({"message": "File uploaded successfully", "file_url": file_url})

        return JsonResponse({"error": "No file provided"}, status=400)

    elif request.method == "GET" and file_id:
        # Retrieve the file from the database using the file ID
        file_instance = get_object_or_404(UploadedFile, id=file_id)
        
        # Serve the file for download (using the stored file path)
        with open(file_instance.file.path, 'rb') as f:  # Use file.path to get the local path
            file_data = f.read()

        response = HttpResponse(file_data, content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="{file_instance.file_name}"'
        return response

    return JsonResponse({"error": "Invalid request"}, status=400)



