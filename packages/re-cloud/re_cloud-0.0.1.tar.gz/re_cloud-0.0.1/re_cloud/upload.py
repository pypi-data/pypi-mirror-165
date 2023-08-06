from pathlib import Path
import pdb
from re_cloud.config.utils import read_re_data_config
import requests
import json
import time
import base64
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.SHA256 as SHA256
import mimetypes

class UploadType:
    DBT = 'DBT_DOCS'
    RE_DATA = 'RE_DATA_OVERVIEW'
    PANDAS_PROFILING = 'PANDAS_PROFILING'
    GREAT_EXPECTATIONS = 'GREAT_EXPECTATIONS'


def get_id_token(service_account_path, iap_client_id):
    oauth_token_uri="https://www.googleapis.com/oauth2/v4/token"
    with open(service_account_path, 'r') as f:
        service_account = json.load(f)
    private_key_id = service_account.get('private_key_id')
    client_email = service_account.get('client_email')
    private_key = service_account.get('private_key')
    issued_at = time.time()
    expires_at = issued_at + 3600
    header= f"{{'alg':'RS256','typ':'JWT','kid':'{private_key_id}'}}"
    header_base64 = base64.urlsafe_b64encode(header.encode('utf-8')).decode('utf-8')
    payload=f"{{'iss':'{client_email}','aud':'{oauth_token_uri}','exp':{expires_at},'iat':{issued_at},'sub':'{client_email}','target_audience':'{iap_client_id}'}}"
    payload_base64 = base64.urlsafe_b64encode(payload.encode('utf-8')).decode('utf-8')
    key = RSA.importKey(private_key)
    # Create an PKCS1_v1_5 object
    signer = PKCS1_v1_5.new(key)
    msg_hash = SHA256.new((header_base64 + "." + payload_base64).encode('utf-8'))
    signature_base64 = base64.urlsafe_b64encode(signer.sign(msg_hash)).decode('utf-8')
    jwt_complete = (header_base64 + "." + payload_base64 + "." + signature_base64).encode('utf-8')
    data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': jwt_complete}
    r = requests.post(url="https://accounts.google.com/o/oauth2/token",data=data)
    r = r.json()
    return r.get('id_token')

def upload_files(upload_type, target, name, file_paths=None):
    config = read_re_data_config()
    re_cloud_config = config.get('re_cloud')
    BASE_URL = re_cloud_config.get('base_url')
    API_KEY = re_cloud_config.get('api_key')
    PROJECT_ID = re_cloud_config.get('project_id')
    SERVICE_ACCOUNT_PATH = re_cloud_config.get('service_account_path')
    IAP_CLIENT_ID = re_cloud_config.get('iap_client_id')
    is_staging_environment = BASE_URL.startswith('https://staging.getre.io')
    headers = {
        'Content-Type': 'application/json'
    }
    if is_staging_environment:
        print('Staging environment detected, attempting to retrieve IAP id_token')
        signed_jwt = get_id_token(SERVICE_ACCOUNT_PATH, IAP_CLIENT_ID)
        print('Retrieved IAP id_token')
        headers['Authorization'] = f'Bearer {signed_jwt}'

    request_data = {
        "api_key": API_KEY,
        "project_id": PROJECT_ID,
        "upload_type": upload_type
    }
    if name: request_data['name'] = name
    if upload_type == UploadType.GREAT_EXPECTATIONS: request_data['file_paths'] = file_paths
    r = requests.post(f'{BASE_URL}/uploads', json=request_data, headers=headers)
    if r.status_code != 200:
        print('Upload failed---')
        print(r.text)
        return
    response = r.json()
    response_data = response.get('data')
    if response.get('status') != 'success':
        print('Upload failed')
        print(r.text)
        return
    upload_data = response_data.get('upload') or {}
    upload_urls = response_data.get('upload_urls') or {}
    
    if upload_type in [UploadType.DBT, UploadType.RE_DATA, UploadType.GREAT_EXPECTATIONS]:
        upload_artefacts_from_directory(target, upload_urls)

    elif upload_type == UploadType.PANDAS_PROFILING:
        upload_file(target, upload_urls.get('index.html'))

    request_data = {
        "api_key": API_KEY
    }
    r = requests.put(f"{BASE_URL}/uploads/{upload_data['id']}/overview/", json=request_data, headers=headers)
    if r.status_code != 200:
        print('Upload failed')
        print(r.text)
        return
    
    print(f"Storage path is {upload_data.get('storage_path')}")


def upload_file(target_file, upload_url):
    mimetype = mimetypes.guess_type(target_file)[0] or 'application/octet-stream'
    with open(target_file, 'rb') as f:
        data = f.read()
        res = requests.put(url=upload_url,
            data=data,
            headers={'Content-Type': mimetype})
        msg = f"""
            Status code is {res.status_code}

            Uploaded {target_file} successfully!
        """
        print(msg)
        print('*' * 80)    


def upload_artefacts_from_directory(target_dir, upload_urls):
    for artefact, upload_url in upload_urls.items():
        file_location = f'{target_dir}/{artefact}'
        if Path(file_location).is_file():
            upload_file(file_location, upload_url)

