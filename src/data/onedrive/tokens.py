import re


refresh_token = None
client_id = None
redirect_uri = None
client_secret = None

def set_token(**kwargs):
    global refresh_token, client_id, redirect_uri, client_secret
    refresh_token = kwargs.get('refresh_token')
    client_id = kwargs.get('client_id')
    redirect_uri = kwargs.get('redirect_uri')
    client_secret = kwargs.get('client_secret')
    return True