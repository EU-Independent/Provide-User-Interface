from django.http import JsonResponse
import requests
from datetime import datetime, timezone
import urllib.parse
from django.conf import settings 


connector_url = settings.CONNECTOR_URL


def convert_date_format(date_str):

    if isinstance(date_str, datetime):
        date_object = date_str
    else:
        try:
            
            date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        except ValueError as e:
            
            print(f"Error: Invalid date format - {e}")
            raise ValueError("Invalid date format")
    
    
    date_object = date_object.replace(tzinfo=timezone.utc)
    
    formatted_date_str = date_object.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"
    return formatted_date_str

def make_request(url, headers=None, body=None):
    try:
        response = requests.post(url, headers=headers, json=body, verify=settings.ENFORCE_CONNECTOR_SSL)
        response_json = response.json()
        if response.status_code in [200, 201]:
            return {
                'status': 'success',
                'data': response_json
            }
        else:
            return {
                'status': 'error',
                'data': response_json
            }
    except requests.RequestException as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def create_catalog(metadata):
    url = settings.CONNECTOR_URL.rstrip('/') + '/api/catalogs'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    title = metadata.get("title")
    description = metadata.get("description")

    data = {
        "title": title,
        "description": description 
    }
    return make_request(url, headers=headers, body=data)

def create_representation(metadata):
    url = settings.CONNECTOR_URL.rstrip('/') + '/api/representations'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    title = metadata.get("title")
    description = metadata.get("description")
    language = metadata.get("language")
    mediaType = metadata.get("mediaType")
    data = {
        "title": title,
        "description": description,
        "language": language,
        "mediaType": mediaType
    }
    return make_request(url, headers=headers, body=data)


def create_offer(metadata):
    url = settings.CONNECTOR_URL.rstrip('/') + '/api/offers'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    title = metadata.get("title")
    description = metadata.get("description")
    keywords = metadata.get("keywords")
    keywords_list = keywords.split(',')
    license = metadata.get("license")
    
    print("license create_offer", license)
    
    paymentMethod = metadata.get("paymentMethod")
    data = {
        "title": title,
        "description": description,
        "keywords": keywords_list,
        "paymentMethod": paymentMethod,  # TODO: paymentMethod 'free' or 'undefined'
        "license": license
    }
    return make_request(url, headers=headers, body=data)


def add_resource_to_catalog(created_catalog_id, created_resource_url):
    url = f"{settings.CONNECTOR_URL.rstrip('/')}/api/catalogs/{created_catalog_id}/offers"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    data = [
        f"{settings.CONNECTOR_URL.rstrip('/')}/api/offers/{created_resource_url}"
    ]
    return make_request(url, headers=headers, body=data)

def add_representation_to_resource(created_resource_id, created_representation_url):
    url = f"{settings.CONNECTOR_URL.rstrip('/')}/api/offers/{created_resource_id}/representations"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    data = [
        f"{settings.CONNECTOR_URL.rstrip('/')}/api/representations/{created_representation_url}"
    ]
    return  make_request(url, headers=headers, body=data)

def create_contract(metadata):
    url = settings.CONNECTOR_URL.rstrip('/') + '/api/contracts'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    title = metadata.get("title")
    description = metadata.get("description")
    start = metadata.get("start")
    end = metadata.get("end")
    data = {
        "title": title,
        "description": description,
        "start": convert_date_format(start), 
        "end": convert_date_format(end)  
    }

    return  make_request(url, headers=headers, body=data)

def create_rule(metadata):
    url = settings.CONNECTOR_URL.rstrip('/') + '/api/rules'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    title = metadata.get("title")
    description = metadata.get("description")
    policy = metadata.get("value")

    data = {
        "title": title,
        "description": description,
        "value": policy
    }
    
    return  make_request(url, headers=headers, body=data)

def add_rule_to_contract(created_contract_id, created_rule_url):
    url = f"{settings.CONNECTOR_URL.rstrip('/')}/api/contracts/{created_contract_id}/rules"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    data = [
        f"{settings.CONNECTOR_URL.rstrip('/')}/api/rules/{created_rule_url}"
    ]

    return  make_request(url, headers=headers, body=data)

def add_contract_to_resource(created_resource_id, created_contract_url):
    url = f"{settings.CONNECTOR_URL.rstrip('/')}/api/offers/{created_resource_id}/contracts"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    data = [
        f"{settings.CONNECTOR_URL.rstrip('/')}/api/contracts/{created_contract_url}"
    ]
    return  make_request(url, headers=headers, body=data)

def create_artifact(metadata):
    url = settings.CONNECTOR_URL.rstrip('/') + '/api/artifacts'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    title = metadata.get("title")
    description = metadata.get("description")
    accessUrl = metadata.get("accessUrl")
    print("create_artifact accessUrlaccessUrlaccessUrl", accessUrl)

    automatedDownload = metadata.get("automatedDownload")
    data = {
        "title": title,
        "description": description,
        "accessUrl": accessUrl,
        "automatedDownload": automatedDownload
    }
    return  make_request(url, headers=headers, body=data)

def add_artifact_to_representation(created_representation_id, created_artifact_url):
    url = f"{settings.CONNECTOR_URL.rstrip('/')}/api/representations/{created_representation_id}/artifacts"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    data = [
        f"{settings.CONNECTOR_URL.rstrip('/')}/api/artifacts/{created_artifact_url}"
    ]
    return  make_request(url, headers=headers, body=data)

def process_creation(create_function, metadata, name):
    result = create_function(metadata)
    print("Status:", result.get('status'))

    # Check if creation was successful
    if result.get('status') == 'success':
        data = result.get('data', {})
        #print("Data:", data)
        #print("Metadata:", list(metadata.values()))

        # Extract and print URL and ID
        url = data.get('_links', {}).get('self', {}).get('href')
        if url:
            item_id = url.split('/')[-1]
            print(f"Created {name} URL:", url)
            print(f"Created {name} ID:", item_id)
        else:
            print(f"Key '_links' or 'self' not found in {name} response data.")
    else:
        print(f"{name} creation failed.")
    
    # Final check
    if url and item_id:
        print(f"{name} URL and ID are valid.")
    else:
        print(f"{name} URL or ID is missing.")
    return url, item_id

def process_addition(operation_name, add_function, *args):
    result = add_function(*args)
    status = result.get('status')
    print(f"Status of {operation_name}:", status)
    return status


def runner(user_metadata):
    # Catalog
    catalog_metadata = user_metadata.get('catalog', {})
    created_catalog_url, created_catalog_id = process_creation(create_catalog, catalog_metadata, "Catalog")
    

    # Representation
    representation_metadata = user_metadata.get('representation', {})
    created_representation_url, created_representation_id = process_creation(create_representation, representation_metadata, "Representation")
    
    
    # Offer
    offer_metadata = user_metadata.get('offer', {})
    created_resource_url, created_resource_id = process_creation(create_offer, offer_metadata, "Offer")

    # Adding Resource to Catalog
    process_addition("Add Resource to Catalog", add_resource_to_catalog, created_catalog_id, created_resource_url)
  
    # Adding Representation to Resource
    process_addition("Add Representation to Resource", add_representation_to_resource, created_resource_id, created_representation_url)

    # Contract
    contract_metadata = user_metadata.get('contract', {})
    created_contract_url, created_contract_id = process_creation(create_contract, contract_metadata, "Contract")

    # Rule
    rule_metadata = user_metadata.get('rule', {})
    created_rule_url, created_rule_id = process_creation(create_rule, rule_metadata, "Rule")

    # Adding rule to contract
    process_addition("Add Rule to Contract", add_rule_to_contract, created_contract_id, created_rule_url)

    # Adding contract to resource
    process_addition("Add Contract to Resource", add_contract_to_resource, created_resource_id, created_contract_url)
    
    # Artifact
    artifact_metadata = user_metadata.get('artifact', {})
    created_artifact_url, created_artifact_id = process_creation(create_artifact, artifact_metadata, "Artifact")

    # Adding artifact to representation
    
    offer_created_successfully = process_addition("Add Artifact to Representation", add_artifact_to_representation, created_representation_id, created_artifact_url)
    
    if offer_created_successfully == 'success':
        return True
    else:
        return False
