import requests
import pandas
from bs4 import BeautifulSoup
import requests
import html5lib
import datetime
from datetime import date
from datetime import datetime as dt

days = ["понедельник", "вторник", "среда", "четверг", "пятница", 'суббота', 'воскресенье']


def day_number():
    return date.weekday(dt.now())


def current_week():
    html = requests.get('http://miu.by/rus/schedule/schedule.php').text
    soup = BeautifulSoup(html, 'html5lib')
    # во всех div найти span, где первый элемент "ТЕКУЩАЯ НЕДЕЛЯ: N",
    # откидываем первые 17 символов
    return [span for div in soup('div') for span in div('span')][1].text[17:]


def weekday(date_str):
    """создает новый столбец со значениями from '08/01/20' to 'среда' и т.д."""
    format_str = '%d/%m/%y'
    datetime_obj = datetime.datetime.strptime(date_str, format_str)
    day_number_ = datetime_obj.weekday()
    return days[day_number_]


def schedule_csv(week=current_week()):
    expschedule_url = "http://miu.by/rus/schedule/expshedule.php"
    payload = {'spec': 'Программное обеспечение информационных технологий'.encode('windows-1251'),
               'group': '181701зд'.encode('windows-1251'),
               'week': week}
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
    formatted_csv['Weekday'] = formatted_csv['Start Date'].apply(weekday)
    return formatted_csv


def schedule_parameters(message):
    if message != 'пары':
        message_parameter = message[5:]
    else:
        return schedule(days[day_number()], schedule_csv())

    if message_parameter in ['на всю неделю', 'неделя']:
        return week_schedule()

    elif message_parameter in ['на следующую неделю', 'след нед']:
        return week_schedule(int(current_week())+1)

    elif message_parameter == 'завтра':
        return schedule(days[day_number()+1], schedule_csv())

    elif message_parameter in days:
        return schedule(days[days.index(message_parameter)], schedule_csv())
    else:
        return 'Извините, я вас не понимаю'


def schedule(day, schedules):
    """собирает пары на конкретный день недели"""
    result_schedule = []
    day_mask = schedules['Weekday'] == day
    day_schedule = schedules[day_mask]

    for index, rows in day_schedule.iterrows():
        start_end = f'{rows["Start Time"][:-6]}-{rows["End Time"][:-6]}'
        description = f'{rows["Description"][:-5]}'
        location = f'{rows["Location"][4:]}'
        result_schedule.append(f'{start_end} {description} {location}')

    if len(result_schedule) == 0:
        return f'{day.capitalize()}:\n В этот день пар нет\n'
    else:
        return f'{day.capitalize()}:\n' + '\n'.join(result_schedule) + '\n'


def week_schedule(week=int(current_week())):
    week_schedule_ = []
    for day in days:
        schedules = schedule(day, schedule_csv(week=week))
        if len(schedules) == 0:
            week_schedule_.append(day.capitalize() + ':\nВ этот день пар нет\n')
            continue
        week_schedule_.append(schedules)
    return '\n'.join(week_schedule_)


