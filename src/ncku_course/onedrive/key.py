import requests



from .exceptions import Unauthorized, APIError


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

    if res.status_code != 200:
        try:
            error_data = res.json()
            error_msg = error_data.get('error_description', error_data.get('error', res.text))
        except Exception:
            error_msg = res.text
            
        if res.status_code == 401:
            raise Unauthorized(f"Failed to refresh token: {error_msg}")
        else:
            raise APIError(f"Failed to refresh token (Status {res.status_code}): {error_msg}")

    result = res.json()
    
    try:
        access_token = result['access_token']
        refresh_token = result['refresh_token']
    except KeyError as e:
        raise APIError(f"Token refresh response missing expected key: {e}. Response: {result}")
    
    return access_token, refresh_token
