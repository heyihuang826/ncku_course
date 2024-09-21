from typing import Union
import requests
import time
import re
import tensorflow as tf
from .captcha.predict import decode_single_sample , ctc_loss, int_to_char
from tensorflow.keras.models import load_model # type: ignore
from .captcha.predict import batch_size, max_label_length, ctc_loss
import os



current_dir = os.path.dirname(os.path.abspath(__file__))

def get_captcha_code(data) -> str:
    model = load_model(current_dir + './captcha/model_20240828_2152', custom_objects={'ctc_loss': ctc_loss})
    pred_label = decode_single_sample(model, data, int_to_char)
    
    return pred_label

def crash_session(session):
    url = 'https://course.ncku.edu.tw/index.php?c=qry11215&m=en_query'
    for i in range(50): 
        res = session.post(url)
        if id_ := get_code_ticket_id(str(res.text)):
            return res, id_
    raise Exception("can not crash site.")

def get_code_ticket_id(text):
    match = re.search(r'code_ticket=([a-zA-Z0-9]{32})&', text)

    if match:
        return str(match.group(1))
    
    return False

def verify_session(session, code_ticket, code):
    url = 'https://course.ncku.edu.tw/index.php?c=portal&m=robot'
    time_num = int(time.time())
    payload = {'time': f'{time_num}', 
               'code_ticket': f'{code_ticket}', 
                'code': f'{code}'}
    session_cookies = session.cookies.get_dict()
    headers = {
         'Accept': '*/*',
         'Content-Length': '74', 
         'Accept-Encoding': 'gzip, deflate, br, zstd',
         'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-US;q=0.7,zh-CN;q=0.6',
         'Cache-Control': 'no-cache',
         'Connection': 'keep-alive',
         'Host': 'course.ncku.edu.tw',
         'X-Requested-With': 'XMLHttpRequest', 
         'Pragma': 'no-cache',
         'referer': 'https://course.ncku.edu.tw/index.php?c=qry11215&m=en_query', 
         'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
         'Sec-Ch-Ua-Mobile': '?0',
         'Sec-Ch-Ua-Platform': '"Windows"',
         'Sec-Fetch-Dest': 'empty',
         'Sec-Fetch-Mode': 'cors',
         'Sec-Fetch-Site': 'same-origin',
         'Sec-Fetch-User': '?1',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 
         'Cookie': f'PHPSESSID={session_cookies["PHPSESSID"]}; COURSE_WEB={session_cookies["COURSE_WEB"]}'
         }
    
    res = session.post(url, headers=headers, data = payload, timeout=10)
    
    return bool(res.json()['status'])

def authenticate(try_limit : int = 10):
    session = requests.Session()
    _, code = crash_session(session)
    for _ in range(try_limit):
        res = session.get(f'https://course.ncku.edu.tw/index.php?c=portal&m=robot&{int(time.time())}')
        content = res.content
        label = get_captcha_code(content)
        success = verify_session(session, code, label.upper())
        if success:
            return session
        
    return False