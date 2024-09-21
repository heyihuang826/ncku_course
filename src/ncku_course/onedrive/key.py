# %%
import requests



def refresh(refresh_token: str, client_id: str, 
            redirect_uri: str, client_secret: str) -> 'tuple[str, str]':    
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    res = requests.post(url, data=data)
    
    result = res.json()
    
    access_token = result['access_token']
    refresh_token = result['refresh_token']
    
    return access_token, refresh_token
# %%
