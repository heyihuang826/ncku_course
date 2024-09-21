# %%
from io import BytesIO
from typing import Union
import requests
from openpyxl import Workbook
from .exceptions import APIError
from ._internal_utils import handle_API_error

def get_upload_url(access_token: str, path: str = "/test/untitled") -> str:
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:{path}:/createUploadSession"
    data = {
      "description" : "description",
      "name" : path.split('/')[-1].split('.')[0],
      "Content-Type" : "application/json"
    }
    
    res = requests.post(url, headers = {"Authorization": access_token}, json = data)
    if res.status_code == 200:
        upload_url = res.json()['uploadUrl']
        return upload_url
    
    raise handle_API_error(res)

def send_file_stream(data, size : int, url) -> Union[bool, APIError]:
    headers = {'Content-Length': str(size), 'Content-Range': f'bytes 0-{str(size - 1)}/{str(size)}'}
    res = requests.put(url, headers=headers, data=data)
    if res.status_code in [200, 201]:
        return True
    
    raise handle_API_error(res)

def upload_with_path(upload_url: str, file_path: str) -> None:
    '''
    upload with file path
    '''
    with open(file_path, 'rb') as f:
        data = f.read()
        size = len(data)
        send_file_stream(data, size, upload_url)
        
def upload_with_bytesio(upload_url: str, file : BytesIO) -> None:
    '''
    upload with `BytesIO` object
    '''
    size = file.getbuffer().nbytes
    data = file.getbuffer()
    
    send_file_stream(data, size, upload_url)
# %%
