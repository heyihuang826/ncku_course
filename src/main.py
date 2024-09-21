from tracemalloc import start
from ncku_course.run import run
from ncku_course.onedrive import set_token
from dotenv import load_dotenv
import time
import sys



start = time.time()

if len(sys.argv) == 5:
    refresh_token = sys.argv[1]
    client_id = sys.argv[2]
    redirect_uri = sys.argv[3]
    client_secret = sys.argv[4]
else:
    load_dotenv(dotenv_path='./.env')
    import os

    client_id = str(os.getenv('client_id'))
    redirect_uri = str(os.getenv('redirect_uri'))
    client_secret = str(os.getenv('client_secret'))
    refresh_token = str(os.getenv('refresh_token'))
    
set_token(refresh_token = refresh_token, client_id = client_id, 
          redirect_uri = redirect_uri, client_secret = client_secret)
run(save = 'both')
print(time.time() - start)