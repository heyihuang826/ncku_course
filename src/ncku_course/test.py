import os
from onedrive import token
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')



client_id = str(os.getenv('client_id'))
redirect_uri = str(os.getenv('redirect_uri'))
client_secret = str(os.getenv('client_secret'))
refresh_token = str(os.getenv('refresh_token'))

print(token(refresh_token, client_id, redirect_uri, client_secret))

