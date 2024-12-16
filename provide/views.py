import requests
from django.shortcuts import render, redirect
from .forms import UploadMetadataForm
from .connector import runner
from django.contrib import messages
from django.conf import settings

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

    incident_id = request.GET.get('incident_id')  # Get incident ID from query parameters
    print("Incident ID: ", incident_id)
    incident_data = {}
    metadata_data = {}

    # Fetch Incident and Metadata Data from a single endpoint
    if incident_id:
        try:
            # Endpoint for fetching incident and metadata data
            incident_url = f"{settings.CYBER_OPERATIONS_INCIDENTS_URL.rstrip('/')}/incident-json/{incident_id}/"

            # Fetch Incident and Metadata Data
            response = requests.get(incident_url,  verify=settings.ENFORCE_CONNECTOR_SSL)
            response.raise_for_status()
            data = response.json().get('data', {})

            incident_data = data.get('incident', {})
            metadata_data = data.get('metadata', {})

        except requests.RequestException as e:
            messages.error(request, f"Failed to load data for incident {incident_id}: {e}")

    # Prepopulate the form with fetched data
    initial_data = {
        'offer_title': "Title",
        'offer_description': metadata_data.get('offer_description', ''),
        'keywords': metadata_data.get('keywords', ''),
        'offer_publisher': metadata_data.get('publisher', ''),
        'offer_language': metadata_data.get('language', ''),
        'offer_license': metadata_data.get('license', ''),
        'accessUrl': 'TeSTGIN',
    }

    print("Initial Data Now: ", incident_url)
    
    if request.method == 'POST':
        form = UploadMetadataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

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
                    'license': data.get('offer_license'),
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

            # Send user metadata to the runner
            result = runner(user_metadata)
            if result:
                messages.success(request, "The offer was successfully provided to the data space.")
            else:
                messages.error(request, "Something went wrong with providing the offer.")

            return redirect('provide_offer')  # Redirect to clear the form and avoid resubmission
        else:
            messages.error(request, "Form is invalid. Please correct the errors and try again.")
    else:
        form = UploadMetadataForm(initial=initial_data)  # Populate form with initial data

    return render(request, 'provide/provide_offer.html', {
        'form': form,
        'fixed_policy_rule': fixed_policy_rule,
        'incident_id': incident_id,
        'incidents_url': settings.CYBER_OPERATIONS_INCIDENTS_URL.rstrip('/'),
    })
