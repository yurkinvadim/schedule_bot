import requests
import pandas

expschedule_url = "http://miu.by/rus/schedule/expshedule.php"
payload = {'spec': 'Программное обеспечение информационных технологий'.encode('windows-1251'),
           'group': '161701с'.encode('windows-1251'),
           'week': '19'}
headers = {"Content-type": "application/x-www-form-urlencoded"}
csv = requests.request("POST", url=expschedule_url, headers=headers, data=payload)

def schedule_parameters():
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
#
