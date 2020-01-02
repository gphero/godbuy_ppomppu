# 1. 스크래핑
# 2. sqlite 에 insert
# 3. 카톡 전송

from selenium import webdriver
import sqlite3
import os
import pyautogui as pag
import time
import threading
import datetime
import pyperclip
from urllib.parse import urlparse, parse_qs

pppomList = []
# 필터
target_list = ['해피머니', '컬쳐랜드', '컬처랜드', '컬쳐캐쉬', '컬처캐쉬', '페이코상품권', '페이코 상품권', 'happymoney', 'happy money',
               'culture land', 'cultureland', 'culture cash', 'culturecash']

# mouse click
def move_and_click(coords):
    pag.moveTo(x=coords[0]+10, y=coords[1]+10, duration=0.0)
    pag.click()

# 키보드 버튼 누르기
def press_button(button_code):
    pag.press(button_code)

def thread_run():
    print('=====', time.ctime(), '=====')
    cherryPicking()
    threading.Timer(30, thread_run).start()

def make_request(today):
    try:
        url = 'http://m.ppomppu.co.kr/new/bbs_list.php?id=ppomppu' # 모바일 뽐뿌게시판
        driver = webdriver.Chrome("./chromedriver.exe")
        driver.get(url)

        for x in range(1, 10) :
            title_result = driver.find_elements_by_xpath('//*[@id="wrap"]/div[4]/div[4]/ul[1]/li['+ str(x) +']/a/div[2]/ul/li[1]/span[1]')
            _title = title_result[0].text

            for element in target_list:
                if element in _title: #제목 필터 걸리면
                    print(_title)
                    url_result = driver.find_elements_by_xpath('// *[ @ id = "wrap"] / div[4] / div[4] / ul[1] / li['+ str(x) +'] / a')
                    _url = url_result[0].get_property('href')
                    print(_url)
                    parsed_url = urlparse(_url)
                    parsed_qs = parse_qs(parsed_url.query)
                    _number = parsed_qs['no'][0]
                    print(_number)

                    pppomList.append((_number, _title, _url, 'N', today))  # number text UNIQUE, title text, url text, sendYn text, date text

        #for search_content in search_result.count():
        #    print(search_content)

    except Exception as e:
        print(e)
        # 카톡 대화방에 오류 났음을 알림
        _title = "Who am I?"
        pyperclip.copy(_title)
        pag.hotkey('ctrl', 'v')
        pag.press('enter')

    finally:
        driver.close()

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dt = datetime.datetime.now()

def cherryPicking():
    today = str(dt.year)  + str(dt.month) + str(dt.day)
    print(today)

    # 1. 스크래핑
    make_request(today)

    # print(my_titles[0])
    #print(my_urls[0])

    # 2. sqlite 에 insert
    conn = sqlite3.connect("ppomList.db")
    with conn:
        cur = conn.cursor()
        #KEY 같으면 무시
        sql = "insert OR IGNORE into ppomList(number, title, url, sendYn, date ) values (?, ?, ?, ?, ?)"
        cur.executemany(sql, pppomList)

        conn.commit()

        cur.execute("select * from ppomList where sendYn = 'N' and date = " + today)
        rows = cur.fetchall()
        #print(type(rows))
        #

    # 4. 카톡 전송
    if len(rows) > 0 :
        #Nprint(rows)
        for row in rows:
            print(row)
            _number = row[0]
            _title = row[1]
            _url = row[2]

            # 4-1. 카톡 대화방에 입력
            pyperclip.copy(_title)
            pag.hotkey('ctrl', 'v')
            pag.press('enter')
            pyperclip.copy(_url)
            pag.hotkey('ctrl', 'v')
            pag.press('enter')

            #4-1. 메시지 보냈으면 sendYn = N으로 update
            conn = sqlite3.connect("ppomList.db")
            with conn:
                cur = conn.cursor()
                query = "UPDATE ppomList SET sendYn = 'Y' WHERE number =" + _number
                cur.execute(query)
                conn.commit()



if __name__ == '__main__':
    thread_run()
