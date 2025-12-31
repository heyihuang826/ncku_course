import time
from typing import List
import requests
from bs4 import BeautifulSoup
from .const import dept_codes

BASE_URL = 'https://course-query.acad.ncku.edu.tw'


def load_home_page(sess: requests.Session):
    # print('cookies', sess.cookies.get('PHPSESSID', ''))
    url = 'https://course-query.acad.ncku.edu.tw/index.php?c=qry11215&m=en_query'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        # 'Accept-Language': 'zh-TW,zh;q=0.9',
        # 'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        'Host': 'course-query.acad.ncku.edu.tw',
        'Pragma': 'no-cache',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'none',
        # 'Sec-Fetch-User': '?1',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # 'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
    }
    res = sess.get(url, headers=headers)
    # print("[*] GET", url)
    # print(res)
    # print("首頁 Set-Cookie:", res.headers.get("Set-Cookie"))
    # print("目前 cookies:", sess.cookies.get_dict())

    return res.text


def save_query(sess: requests.Session, dept_code: str):
    # print('cookies', sess.cookies.get('PHPSESSID', ''))
    url = "https://course-query.acad.ncku.edu.tw/index.php?c=qry11215&m=save_qry"
    headers = {
        'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        # 'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '74',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': f"PHPSESSID={sess.cookies.get('PHPSESSID', '')}",
        # 'Host': 'course-query.acad.ncku.edu.tw',
        'Origin': 'https://course-query.acad.ncku.edu.tw',
        # 'Pragma': 'no-cache',
        'Referer': 'https://course-query.acad.ncku.edu.tw/index.php?c=qry11215&m=en_query',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        # 'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
    }
    payload = {
        'id': '94',
        'cosname': '',
        'teaname': '',
        'syear_b': '114',
        'syear_e': '114',
        'sem_b': '2',
        'sem_e': '2',
        'dept_no': dept_code
    }
    res = sess.post(url, headers=headers, data=payload)
    # print("[*] POST", url)
    # print(res)

    return res


def fetch_js(sess: requests.Session, js_path: str):
    url = BASE_URL + js_path
    headers = {
        'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        # 'Accept-Language': 'zh-TW,zh;q=0.9',
        # 'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=582e9bfe93c01630e30d993af919b231',
        'Host': 'course-query.acad.ncku.edu.tw',
        # 'Pragma': 'no-cache',
        'Referer': 'https://course-query.acad.ncku.edu.tw/index.php?c=qry11215&m=en_query',
        # 'Sec-Fetch-Dest': 'script',
        # 'Sec-Fetch-Mode': 'no-cors',
        # 'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # 'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
    }
    res = sess.get(url, headers=headers)
    # print("[*] GET", url)
    # print(res)

    return res


def get_time(times):
    frame = [0 for i in range(112)]

    def to_frame(date, start_time, end_time):
        move = 0
        dic_time = {'0': 0,
                    '1': 1,
                    '2': 2,
                    '3': 3,
                    '4': 4,
                    'N': 5,
                    '5': 6,
                    '6': 7,
                    '7': 8,
                    '8': 9,
                    '9': 10,
                    'A': 11,
                    'B': 12,
                    'C': 13,
                    'D': 14,
                    'E': 15
                    }

        start_time = dic_time[start_time]
        end_time = dic_time[end_time]
        for i in range(start_time, end_time + 1):
            frame[(date - 1) * 16 + i + move] = 1

    for i in times:
        if (i == ''):
            return [0 for i in range(112)]
        if (i[0] != '['):
            continue
        i = i[1:].split(']')
        date = int(i[0])
        time = i[1].split('~')
        if (len(time) == 2):
            to_frame(date, time[0], time[1])
        elif (len(time) == 1):
            if (time[0] == ''):
                return [0 for i in range(112)]
            to_frame(date, time[0], time[0])
        else:
            raise Exception("程式發生錯誤, 請聯絡開發者(錯誤代碼:0x00000004)")
    return frame

def get_info_from_res(res) -> List:
    result = []
    soup = BeautifulSoup(res.text, 'lxml')
    table = soup.find('table', {'id': 'A9-table'})

    trs = table.tbody.find_all('tr', recursive=False)  # type: ignore

    for n in range(len(trs)):  # 遍歷各課程列資料
        tds = trs[n].find_all('td', recursive=False)
        if (len(tds) != 11): # 歷年查詢多了學年期
            raise Exception("程式發生錯誤, 請聯絡開發者(錯誤代碼:0x00000005)")
        # 系所名稱
        depart_name = tds[1].text

        # '系號序號', '課程碼分班碼', '屬性碼'
        dept_id = tds[2].find(
            'div', {'class': 'dept_seq'}, recursive=False).text
        course_code, attribute_code = map(str, tds[2].text.split()[-2:])

        # if dept_id[:2] not in [list(dept_codes.keys())[i], '']:
        #     print(f"dept_id: {dept_id} 收到不符合規則回應，重新執行")
        #     time.sleep(5)
        #     run(i)
        #     return

        if (attribute_code[0] != '[' or attribute_code[-1] != ']'):
            raise Exception("程式發生錯誤, 請聯絡開發者(錯誤代碼:0x00000006)")
        attribute_code = attribute_code[1:-1]

        # '年級', '班別', '組別'
        y, c, g = map(lambda x: x.strip(), str(tds[3]).replace(
            '<td>', '').replace('</td>', '').split('<br/>'))

        # 類別
        Category = tds[4].text

        # 科目名稱
        subject_name = tds[5].find(
            'span', {'class': 'course_name'}, recursive=False).text
        subject_name_full = tds[5].text

        # 學分,選必修
        credit, elective = map(lambda x: x.strip(), str(tds[6]).replace(
            '<td align="center">', '').replace('</td>', '').split('<br/>'))

        # 教師姓名
        teacher_name = str(tds[7]).replace(
            '<td class="sm">', '').replace('</td>', '').split('<br/>')

        # 已選課人數/餘額
        for span_element in tds[8].find_all('span'):
            span_element.decompose()
        num_enrolled, num_remaining = map(
            str, (tds[8].get_text() + '/').split('/')[:2])

        # 時間, 教室
        classroom, time_list = [], []
        temp1, temp2 = '', ''
        for content in tds[9].contents:
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

        # 課綱網址
        temp = tds[10].find('a', string='課程大綱')
        if temp:
            outline_url = temp['href']
        else:
            outline_url = ''

        try:
            result.append([depart_name, dept_id, course_code, attribute_code, y, c, g, Category, subject_name, subject_name_full, credit, elective, str(
                teacher_name), num_enrolled, num_remaining, str(time_list), str(classroom), outline_url] + get_time(time_list))
        except Exception as error_msg:
            print("程式發生錯誤, 請聯絡開發者(錯誤代碼:0x00000003)")  # 加入資料至資料表末端時發生不明錯誤
            if (input().lower() == "debug"):
                print(error_msg)
            while (True):
                time.sleep(1000)

    return result


js_paths = [
    '/bootstrap/js/jquery.min.js',
    '/bootstrap/js/jquery.min.js?20250612',
    '/bootstrap/js/bootstrap.js?20250612',
    '/bootstrap/js/main.js?20250612',
    '/bootstrap/js/wow.min.js?20250612',
    '/bootstrap/js/multimodal.min.js?20250612',
    '/js/modernizr-custom.js?20250612',
    '/js/bootstrap-select/js/bootstrap-select.min.js?20250612',
    '/js/common.js?20250612',
    '/js/mis_grid.js?20250612',
    '/js/performance.now-polyfill.js?20250612',
    '/js/mdb-sortable/js/addons/jquery-ui-touch-punch.min.js?20250612',
    '/js/jquery.taphold.js?20250612',
    '/js/jquery.patch.js?20250612',
    '/js/jquery.cookie.js?20250612',
    '/nf/commons/v2.1.1/js/jquery.blockUI.js?20250612'
]

# sess = requests.Session()
# sess.cookies.set('PHPSESSID', '51d57ccb6560f87912ec485aef6dd108')
# res = load_home_page(sess)
# assert "驗證碼" not in str(res), "偵測到驗證碼檢查"
# assert "正在檢查" not in str(res), "偵測到cloudflare檢查"

# for path in js_paths:
#     res = fetch_js(sess, path)
# res = save_query(sess, '')
# url = 'https://course-query.acad.ncku.edu.tw/index.php?c=qry11215&m=save_qry' + res.text

# print(url)
# res =  sess.get(url)
# result = get_info_from_res(res)
# # print(result)
# print(len(result))


def get_history_data(dept_no: str, sess: requests.Session) -> List:
    res = load_home_page(sess)
    assert "驗證碼" not in str(res), "偵測到驗證碼檢查"
    assert "正在檢查" not in str(res), "偵測到cloudflare檢查"
    for path in js_paths:
        res = fetch_js(sess, path)
    res = save_query(sess, dept_no)
    print(res.text)
    url = 'https://course-query.acad.ncku.edu.tw/index.php?c=qry11215&m=save_qry' + res.text
    res = sess.get(url)
    result = get_info_from_res(res)
    
    # print(f"程式於 {dept_codes[dept_no]} 完成抓取 {len(result)} 筆課程資料")
    
    return result


# print(len(get_history_data('', sess)))
