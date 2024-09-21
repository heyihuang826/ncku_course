from io import BytesIO
from .crawler import crawler
from .excel import to_excel
from .authenticate import authenticate
import threading
import time
from .const import dept_codes
from .onedrive import token, upload_url, upload



def upload_to_onedrive(file, file_name, **kwargs):
    access_token, _ = token(**kwargs)
    url = upload_url(f"/NCKU_coursesData/{file_name}", access_token) #upload path for onedrive file
    upload(url, file)

def run(save: str = 'local'):
    '''
    save: str
    local: save to local(default)
    onedrive: save to onedrive with provided information in .env or pass by argument
    both: save to both local and onedrive
    '''
    session = authenticate(3)
    # session = requests.Session() #skip robot authentication

    if not session:
        raise Exception("can not authenticate.")

    results = []
    threads = []
    for dept_code in dept_codes:
        t = threading.Thread(target=crawler, args = (results, dept_code, session, ))
        threads.append(t)
        
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()

    excel = to_excel(results)

    file_name = f"data_{time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time() + 8 *3600 - time.localtime().tm_gmtoff))}.xlsx"
    if save in ['both', 'local']: excel.save(file_name)
    if save in ['both', 'onedrive']:
        virtual_workbook = BytesIO()
        excel.save(virtual_workbook)
        upload_to_onedrive(virtual_workbook, file_name)
        
    return file_name