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
            # Try full ISO 8601 parsing (Python 3.7+)
            date_object = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except Exception:
            try:
                # Fallback: try without seconds
                date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
                date_object = date_object.replace(tzinfo=timezone.utc)
            except Exception as e:
                print(f"Error: Invalid date format - {e}")
                raise ValueError("Invalid date format")
    # Always output in connector format: YYYY-MM-DDTHH:MM:SS.sss+0000
    formatted_date_str = date_object.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"
    return formatted_date_str

def _build_auth_components(auth_meta):
    """Return (auth_header_dict, requests_auth) tuple based on auth_meta."""
    if not auth_meta:
        return {}, None
    auth_type = auth_meta.get('auth_type')
    headers = {}
    auth = None
    if auth_type == 'basic':
        username = auth_meta.get('auth_username')
        password = auth_meta.get('auth_password')
        from requests.auth import HTTPBasicAuth
        auth = HTTPBasicAuth(username, password)
    elif auth_type == 'bearer':
        token = auth_meta.get('auth_token')
        headers['Authorization'] = f'Bearer {token}'
    return headers, auth


def make_request(url, headers=None, body=None, method='post', auth_meta=None):
    try:
        auth_headers, auth_obj = _build_auth_components(auth_meta)
        final_headers = dict(headers or {})
        final_headers.update(auth_headers)
        if method.lower() == 'get':
            response = requests.get(url, headers=final_headers, params=body, auth=auth_obj, verify=settings.ENFORCE_CONNECTOR_SSL)
        else:
            response = requests.post(url, headers=final_headers, json=body, auth=auth_obj, verify=settings.ENFORCE_CONNECTOR_SSL)
        try:
            response_json = response.json()
        except ValueError:
            response_json = None
        if response.status_code in [200, 201]:
            return {
                'status': 'success',
                'data': response_json
            }
        else:
            return {
                'status': 'error',
                'status_code': response.status_code,
                'reason': response.reason,
                'data': response_json,
                'text': response.text
            }
    except requests.RequestException as e:
        return {
            'status': 'error',
            'message': str(e)
        }


def test_access_url(access_url, auth_meta=None, timeout=10, method='get'):
    """Perform a lightweight request to the access_url using the provided auth metadata.
    Returns a dict with status and minimal response info.
    """
    try:
        headers, auth = _build_auth_components(auth_meta)
        # perform a GET request by default
        resp = requests.request(method.upper(), access_url, headers=headers, auth=auth, timeout=timeout, verify=settings.ENFORCE_CONNECTOR_SSL)
        try:
            data = resp.json()
        except ValueError:
            data = None
        if resp.status_code >= 200 and resp.status_code < 300:
            return {'status': 'success', 'status_code': resp.status_code, 'reason': resp.reason, 'data': data}
        else:
            return {'status': 'error', 'status_code': resp.status_code, 'reason': resp.reason, 'data': data, 'text': resp.text}
    except requests.RequestException as e:
        return {'status': 'error', 'message': str(e)}

def create_catalog(metadata):
    url = settings.CONNECTOR_URL.rstrip('/') + '/api/catalogs'
    print("create_catalog--------", url)
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
    print("----------create_catalog--------", url)
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
    print("create_offer metadata", metadata)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }
    title = metadata.get("title")
    description = metadata.get("description")
    keywords = metadata.get("keywords")
    keywords_list = keywords.split(',')
    license = metadata.get("license")
    publisher = metadata.get("publisher")
    
    print("license create_offer", license)
    
    paymentMethod = metadata.get("paymentMethod")
    data = {
        "title": title,
        "description": description,
        "keywords": keywords_list,
        "paymentMethod": paymentMethod,  # TODO: paymentMethod 'free' or 'undefined'
        "license": license,
        "publisher": publisher
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
    # forward any auth metadata if present so artifact can carry access credentials
    if metadata.get('auth'):
        data['auth'] = metadata.get('auth')
    # legacy fields
    for k in ('auth_type', 'auth_username', 'auth_password', 'auth_token'):
        if metadata.get(k):
            data[k] = metadata.get(k)
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

    # Initialize variables to avoid UnboundLocalError
    url = None
    item_id = None

    # Check if creation was successful
    if result.get('status') == 'success':
        data = result.get('data', {})
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
