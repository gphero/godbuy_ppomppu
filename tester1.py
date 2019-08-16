# 1. 스크래핑
# 2. sqlite 에 insert
# 3. 카톡 전송

import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import pyautogui as pag
import time
import threading
import datetime
import pyperclip
from urllib.parse import urlparse, parse_qs
# mouse click
def move_and_click(coords):
    pag.moveTo(x=coords[0]-20, y=coords[1], duration=0.0)
    pag.click()

# 키보드 버튼 누르기
def press_button(button_code):
    pag.press(button_code)

def thread_run():
    print('=====', time.ctime(), '=====')
    cherryPicking()
    threading.Timer(30, thread_run).start()

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dt = datetime.datetime.now()

def cherryPicking():
    # 1. 스크래핑
    today = str(dt.year) + str(dt.month) + str(dt.day)
    print( today )
    req = requests.get('http://m.ppomppu.co.kr/new/bbs_list.php?id=ppomppu') # 모바일 뽐뿌게시판
    base_url = 'm.ppomppu.co.kr/new/' # 본 게시물 베이스.
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select( #제목 추출용
        'div.ct > div.bbs > ul > li > a > span'
    )
    my_urls = soup.select( #URL 추출용
        'div.ct > div.bbs > ul > li > a'
    )
    # print(my_titles[0])
    #print(my_urls[0])

    pppomList = []
    # 필터
    target_list = ['해피머니', '컬쳐랜드', '컬처랜드', '컬쳐', '컬처', '컬쳐캐쉬', '컬처캐쉬', 'happy', 'money', 'culture','land', 'cash','JTUM']

    counter = 0
    _title = ''
    _url = ''
    _number = ''
    for title in my_titles:
        #print(title) #<span class="title"> [우체국쇼핑] 진안 시케이푸드 오리불고기 매콤 양념주물럭 오리불고기 500g, 오리양념주물럭 500g (2팩)(14,000/무료) 할인가 13,600</span>
        #data[title.text] = title.get('class') # 제목
        # print(title.text)
        counter = counter + 1
        for element in target_list:
            if element in title.text:
                _title = title.text
                _url = base_url + my_urls[counter].get('href')
                parsed_url = urlparse(_url)
                parsed_qs = parse_qs(parsed_url.query)
                _number = parsed_qs['no']
                print(_number)
                #print(_title) #[우체국쇼핑] 진안 시케이푸드 오리불고기 매콤 양념주물럭 오리불고기 500g, 오리양념주물럭 500g (2팩)(14,000/무료) 할인가 13,600
                #print(_url) # URL  bbs_view.php?id=ppomppu&no=326550&page=1
                pppomList.append((_number, _title, _url, 'N', today)) #number text UNIQUE, title text, url text, sendYn text, date text

    #print(pppomList)


    # 2. sqlite 에 insert
    #중복제거 필요함.
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