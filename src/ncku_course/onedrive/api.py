from io import BytesIO
from os import access
from typing import Union
from .upload import upload_with_bytesio, upload_with_path, get_upload_url
from .key import refresh



def upload(upload_url, file):
    """
    with file path
    with bytesio
    """
    if type(file) == str:
        upload_with_path(upload_url, file)
    elif type(file) == BytesIO:
        upload_with_bytesio(upload_url, file)
    else:
        raise ValueError(f"file type {type(file)} is not supported. Please use str or BytesIO.")

def token():
    """
    refresh access token and refresh token
    
    return: (access_token, refresh_token)
    """
    from .tokens import refresh_token, client_id, redirect_uri, client_secret
    
    if refresh_token is None or client_id is None or redirect_uri is None or client_secret is None:
        raise ValueError("Please set refresh_token, client_id, redirect_uri, client_secret.")
    
    return refresh(refresh_token, client_id, redirect_uri, client_secret)

def set_token(**kwargs):
    """
    set refresh token, client_id, redirect_uri, client_secret
    """
    from .tokens import set_token
    
    return set_token(**kwargs)

def upload_url(path, access_token : str):
    """
    get upload url
    """
    return get_upload_url(access_token, path)
