import requests
import pandas
from bs4 import BeautifulSoup
import requests
import html5lib


def current_week():
    html = requests.get('http://miu.by/rus/schedule/schedule.php').text
    soup = BeautifulSoup(html, 'html5lib')
    # во всех div найти span, где первый элемент "ТЕКУЩАЯ НЕДЕЛЯ: N",
    # откидываем первые 17 символов
    return [span for div in soup('div') for span in div('span')][1].text[17:]


def schedule_parameters():
    expschedule_url = "http://miu.by/rus/schedule/expshedule.php"
    payload = {'spec': 'Программное обеспечение информационных технологий'.encode('windows-1251'),
               'group': '161701с'.encode('windows-1251'),
               'week': current_week()}
# 'week': '19'}
    
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    csv = requests.request("POST", url=expschedule_url, headers=headers, data=payload)
    csv.encoding = 'windows-1251'
    text_file = open("Output.txt", "w")
    text_file.write(csv.text)
    text_file.close()
    try:
        formatted_csv = pandas.read_csv("Output.txt", encoding='utf-8')
    except UnicodeDecodeError:
        formatted_csv = pandas.read_csv("Output.txt", encoding="windows-1251")
    return formatted_csv[["Start Time", "Description", "Location"]].to_string()


