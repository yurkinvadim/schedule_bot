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


def time(time_str):
    """конвертрование формата времени из 12 в 24"""
    format_str = '%I:%M:%S %p'
    convert_format = '%H:%M'
    time = datetime.datetime.strptime(time_str, format_str)
    return f'{time.strftime(convert_format)}'


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
    formatted_csv['Start Time'] = formatted_csv['Start Time'].apply(time)
    formatted_csv['End Time'] = formatted_csv['End Time'].apply(time)
    return formatted_csv


def schedule_parameters(message):
    if message != 'пары':
        message_parameter = message[5:]
    else:
        schedules = schedule(days[day_number()], schedule_csv())
        if len(schedules) == 0:
            return 'Сегодня пар нет'
        else:
            return f'{days[day_number()].capitalize()}:\n' + '\n'.join(schedules) + '\n'

    if message_parameter in ['на всю неделю', 'неделя']:
        week_schedule = []
        for day in days:
            schedules = schedule(day, schedule_csv())
            if len(schedules) == 0:
                week_schedule.append(day.capitalize() + ':\nВ этот день пар нет\n')
                continue
            week_schedule.append(f'{day.capitalize()}:\n'+'\n'.join(schedules)+'\n')
        return '\n'.join(week_schedule)

    elif message_parameter == 'на следующую неделю':
        week_schedule = []
        for day in days:
            schedules = schedule(day, schedule_csv(week=int(current_week())+1))
            if len(schedules) == 0:
                week_schedule.append(day.capitalize() + ':\nВ этот день пар нет\n')
                continue
            week_schedule.append(f'{day.capitalize()}:\n' + '\n'.join(schedules) + '\n')
        return '\n'.join(week_schedule)

    elif message_parameter == 'завтра':
        schedules = schedule(days[day_number()+1], schedule_csv())
        if len(schedules) == 0:
            return 'В этот день пар нет'
        else:
            return f'{days[day_number()+1].capitalize()}:\n' + '\n'.join(schedules) + '\n'

    elif message_parameter in days:
        schedules = schedule(days[days.index(message_parameter)], schedule_csv())
        if len(schedules) == 0:
            return 'В этот день пар нет'
        else:
            return f'{days[days.index(message_parameter)].capitalize()}:\n'+'\n'.join(schedules)+'\n'
    else:
        return 'Извините, я вас не понимаю'


def schedule(day, schedules):
    """собирает пары на конкретный день недели"""
    result_schedule = []
    day_mask = schedules['Weekday'] == day
    day_schedule = schedules[day_mask]

    for index, rows in day_schedule.iterrows():
        start_end = f'{rows["Start Time"]}-{rows["End Time"]}'
        description = f'{rows["Description"][:-5]}'
        location = f'{rows["Location"][4:]}'
        result_schedule.append(f'{start_end} {description} {location}')
    return result_schedule


