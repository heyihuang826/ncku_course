from typing import List
from bs4 import BeautifulSoup
import requests
from .const import dept_codes
import time
from ._inner_utils import get_time
from .excel import to_excel


def get_url(cosname, teaname, wk = '', dept_no = '', degree = '', cl = '') -> str:
    if(wk not in ['1', '2', '3', '4', '5', '6', '7', ''] or
       dept_no not in list(dept_codes.keys()) + [""] or
       degree not in ['1', '2', '3', '4', '5', '6', '7', '']):
        raise Exception('error')
    url = 'https://course.ncku.edu.tw/index.php?c=qry11215&m=save_qry'
    payload ={
        'id': 'CWhUPQU0VTkCfANzADteb1NpCn9VPlRyAz0MZgZqAzxXPlR7UClUIARvVWJXaA4hVXNQcQE4DGFWaFEwCDoEew1wAC4=', 
        'cosname': f'{cosname}', 
        'teaname': f'{teaname}', 
        'wk': f'{wk}', 
        'dept_no': f'{dept_no}', 
        'degree': f'{degree}', 
        'cl': f'{cl}'
        }
    headers = {
        'Accept-Encoding': 'gzip, deflate, br, zstd', 
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-US;q=0.7,zh-CN;q=0.6', 
        'Cache-Control': 'no-cache', 
        'Connection': 'keep-alive', 
        'Content-Length': '141', 
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
        'Host': 'course.ncku.edu.tw', 
        'Origin': 'https://course.ncku.edu.tw', 
        'Pragma': 'no-cache', 
        'Referer': 'https://course.ncku.edu.tw/index.php?c=qry11215&m=en_query', 
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"', 
        'Sec-Ch-Ua-Mobile': '?0', 
        'Sec-Ch-Ua-Platform': '"Windows"', 
        'Sec-Fetch-Dest': 'empty', 
        'Sec-Fetch-Mode': 'cors', 
        'Sec-Fetch-Site': 'same-origin', 
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36', 
        'X-Requested-With': 'XMLHttpRequest'
        }

    res = requests.post(url = url, data=payload, headers=headers)

    if res.status_code != 200:
        raise Exception(f'res error: {res.status_code}')

    return 'https://course.ncku.edu.tw/index.php?c=qry11215' + str(res.text)

def get_info_from_res(res) -> List:
    result = []
    soup = BeautifulSoup(res.text, 'lxml')
    table = soup.find('table', {'id' : 'A9-table'})

    trs = table.tbody.find_all('tr', recursive=False) # type: ignore
    
    for n in range(len(trs)): #遍歷各課程列資料
        tds = trs[n].find_all('td', recursive=False)
        if(len(tds) != 10):
            raise Exception("程式發生錯誤, 請聯絡開發者(錯誤代碼:0x00000005)")
        #系所名稱
        depart_name = tds[0].text
        
        #'系號序號', '課程碼分班碼', '屬性碼'
        dept_id = tds[1].find('div', {'class' : 'dept_seq'}, recursive=False).text
        course_code, attribute_code = map(str, tds[1].text.split()[-2:])
        
        # if dept_id[:2] not in [list(dept_codes.keys())[i], '']:
        #     print(f"dept_id: {dept_id} 收到不符合規則回應，重新執行")
        #     time.sleep(5)
        #     run(i)
        #     return
        
        if(attribute_code[0] != '[' or attribute_code[-1] != ']'):
            raise Exception("程式發生錯誤, 請聯絡開發者(錯誤代碼:0x00000006)")
        attribute_code = attribute_code[1:-1]
        
        #'年級', '班別', '組別'
        y, c, g = map(lambda x : x.strip(), str(tds[2]).replace('<td>', '').replace('</td>', '').split('<br/>'))
        
        #類別
        Category = tds[3].text
        
        #科目名稱
        subject_name = tds[4].find('span', {'class' : 'course_name'}, recursive=False).text
        subject_name_full = tds[4].text
        
        #學分,選必修
        credit, elective = map(lambda x: x.strip(), str(tds[5]).replace('<td align="center">', '').replace('</td>', '').split('<br/>'))
        
        #教師姓名
        teacher_name = str(tds[6]).replace('<td class="sm">', '').replace('</td>', '').split('<br/>')
        
        #已選課人數/餘額
        for span_element in tds[7].find_all('span'):
            span_element.decompose()
        num_enrolled, num_remaining = map(str, (tds[7].get_text() + '/').split('/')[:2])
        
        #時間, 教室
        classroom, time_list = [], []
        temp1, temp2 = '', ''
        for content in tds[8].contents:
            if isinstance(content, str):
                temp1 = content.strip()
            elif content.name == 'a':
                temp2 = content.get_text(strip=True)
            elif content.name == 'br':
                classroom.append([temp1, temp2])
                time_list.append(temp1)
                temp1, temp2 = '', ''
        classroom.append([temp1, temp2])
        time_list.append(temp1)
        
        #課綱網址
        temp = tds[9].find('a', string = '課程大綱')
        if temp:
            outline_url = temp['href']
        else:
            outline_url = ''
        
        try:
            result.append([depart_name, dept_id, course_code, attribute_code, y, c, g, Category, subject_name, subject_name_full, credit, elective, str(teacher_name), num_enrolled, num_remaining, str(time_list), str(classroom), outline_url] + get_time(time_list))
        except Exception as error_msg:
            print("程式發生錯誤, 請聯絡開發者(錯誤代碼:0x00000003)") #加入資料至資料表末端時發生不明錯誤
            if(input().lower() == "debug"):
                print(error_msg)
            while(True):
                time.sleep(1000)
            
    return result
        
def crawler(results : List, dept_no : str, session = None) -> None:
    if not session:
        session = requests.Session()
    url = get_url('', '', dept_no = dept_no)
    res = session.get(url)
    result = get_info_from_res(res)
    print(f"程式於 {dept_codes[dept_no]} 完成抓取 {len(result)} 筆課程資料")
    results.extend(result)

# url = 'https://course-query.acad.ncku.edu.tw/query/index.php?c=qry11215&m=en_query&lang=cht'
# res = requests.get(url)
# with open('res.html', 'w', encoding='utf-8') as f:
#     f.write(res.text)