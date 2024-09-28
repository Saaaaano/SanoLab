from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def get_data_soup(url_data):
    url = url_data
    res = requests.get(url)
    # ソースを取得
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

#表の見出し情報を取得
def get_data_header(soup):
    header_items = []
    names = []
    # スケジュール表を取得
    schedule_table = soup.find('table', {'class': 'listtbl'})
    # 行ごとに分解してリストに格納
    schedule_list = schedule_table.find_all('tr')
    # 表の見出し（1行目）を取得
    schedule_header = schedule_list[0]
    # 日付ごとのマークの数
    header_items_temp = schedule_header.find_all('td', {'class': 'rline'})
    for i in header_items_temp:
        header_items.append(i.text)
    # 記入者の名前
    names_temp = schedule_header.find_all('a')
    for i in names_temp:
        names.append(i.text)
    # 返すのは記入者の名前と日付ごとのマークの数のみ
    return names, header_items

def get_data_schedule(soup, names, header_items):
    # スケジュール表を取得
    schedule_table = soup.find('table', {'class': 'listtbl'})
    # 行ごとに分解してリストに格納
    schedule_list = schedule_table.find_all('tr')
    lines = []
    dates = []
    # 表の見出し以外の部分を抜き出す
    schedule_items = schedule_list[1:]
    for schedule_item in schedule_items:
        # 行内の要素を取得
        date = schedule_item.find('td').text
        dates.append(date)
        attendance_temp = schedule_item.find_all('td')
        # 日付とそれぞれの要素の数は削除する
        attendance_temp = attendance_temp[len(header_items)+1:]
        line = []
        line.append(date)
        for attendance in attendance_temp:
            line.append(attendance.text)
        lines.append(line)
    # 2次元配列を返す
    return lines


def get_expl(soup):
    # イベント説明文を取得
    return soup.find('div', {'class':'explbox'}).text

def get_comment(soup):
    # コメントを取得
    comment = soup.find('div',{'class':"commentbox"}).find('li').text
    comment = comment.strip()
    comment = comment.replace(' ', '')
    comment_list = re.split('[()]', comment)
    return comment_list[1:]
