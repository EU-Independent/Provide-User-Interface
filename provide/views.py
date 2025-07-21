from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .forms import UploadMetadataForm
from .connector import runner
from .models import License, UploadedFile

# Constants
ALLOWED_FILE_TYPES = ["application/json"]
UPLOAD_DIR = 'uploads'


# Helper Functions
def get_license_choices():
    """Retrieve license choices for the form."""
    licenses = License.objects.all()
    return [(license.name, license.name) for license in licenses]


def generate_user_metadata(data, license_url):
    """Generate user metadata for the offer."""
    return {
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


# Views
def provide_offer(request):
    """Provide an offer with metadata."""
    fixed_policy_rule = get_fixed_policy_rule()
    connector_url = settings.CONNECTOR_URL
    license_choices = get_license_choices()
    
    # Prepopulate form data if available
    initial_data = {
        'offer_title': '',
        'offer_description': '',
        'keywords': '',
        'offer_publisher': '',
        'offer_language': '',
        'offer_license': '',
        'accessUrl': '',
    }

    if request.method == 'POST':
        form = UploadMetadataForm(request.POST, license_choices=license_choices)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            selected_license_name = data.get('offer_license')
            selected_license = License.objects.filter(name=selected_license_name).first()
            license_url = selected_license.access_url if selected_license else ""

            user_metadata = generate_user_metadata(data, license_url)
            print("User Metadata: ", user_metadata)

            result = runner(user_metadata)
            if result:
                messages.success(request, "The offer was successfully provided to the data space.")
                #return redirect('survey')  
            else:
                messages.error(request, "Something went wrong with providing the offer.")
            #return redirect('survey')
        else:
            messages.error(request, "Form is invalid. Please correct the errors and try again.")
    else:
        form = UploadMetadataForm(request.POST or None, license_choices=license_choices)

    return render(request, 'provide/provide_offer.html', {
        'form': form,
        'fixed_policy_rule': fixed_policy_rule,
        'licenses': License.objects.all(),
        'data_space_connector_url': connector_url,
    })


def get_fixed_policy_rule():
    """Return the fixed policy rule for the offer."""
    return (
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


@csrf_exempt
def upload_view(request, file_id=None):
    """Handle file upload and retrieval."""
    if request.method == "POST":
        return handle_file_upload(request)
    elif request.method == "GET" and file_id:
        return handle_file_download(file_id)

    return JsonResponse({"error": "Invalid request"}, status=400)


def handle_file_upload(request):
    """Handle the file upload process."""
    if request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        if uploaded_file.content_type not in ALLOWED_FILE_TYPES:
            return JsonResponse({"error": "Invalid file type. Only JSON files are allowed."}, status=400)

        # Create upload directory if not exists
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        # Save file instance
        file_instance = UploadedFile.objects.create(
            file=uploaded_file,
            file_name=uploaded_file.name
        )
        file_url = f"{settings.DOMAIN_URL}{settings.MEDIA_URL}{file_instance.file.name}"
        return JsonResponse({"message": "File uploaded successfully", "file_url": file_url})
    return JsonResponse({"error": "No file provided"}, status=400)


def handle_file_download(file_id):
    """Handle file download request."""
    file_instance = get_object_or_404(UploadedFile, id=file_id)
    with open(file_instance.file.path, 'rb') as f:
        file_data = f.read()

    response = HttpResponse(file_data, content_type="application/json")
    response["Content-Disposition"] = f'attachment; filename="{file_instance.file_name}"'
    return response
