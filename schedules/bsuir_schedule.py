import requests
import json
from datetime import datetime
from datetime import date

url = "https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=613301"
response = (requests.get(url=url)).text
schedule_json = json.loads(response)

day_number = date.weekday(datetime.now())
days = ["понедельник", "вторник", "среда", "четверг", "пятница", 'суббота', 'воскресенье']


def remember_lesson(lesson):
    employee = lesson['employee'][0]
    employee_name = employee['lastName'] + ' ' + employee['firstName'] + ' ' + employee['middleName']
    lesson_time = lesson['lessonTime']
    subject = lesson['subject']
    auditory = lesson['auditory'][0]
    num_subgroup = lesson['numSubgroup']
    lesson_type = lesson['lessonType']
    if num_subgroup == 0:
        num_subgroup = 'обе'
    return f'{lesson_time} {lesson_type} {subject} {employee_name} {auditory}, Подгруппа: {num_subgroup}'


def schedule(day, week=schedule_json['currentWeekNumber']):
    for schedules in schedule_json['schedules']:
        if schedules['weekDay'].lower() == day:
            result_schedule = []
            for lesson in schedules['schedule']:
                if week in lesson['weekNumber']:
                    result_schedule.append(remember_lesson(lesson))
            return '\n'.join(result_schedule)
    return 'В этот день пар нет'


def schedule_parameters(message):
    # сегодняшний день
    if len(message) > 4:
        message_parameter = message[5:]
    else:
        return schedule(days[day_number])

    # конкретный день недели
    if message_parameter in days:
        week = schedule_json['currentWeekNumber']
        if day_number > days.index(message_parameter):
            if schedule_json['currentWeekNumber'] == 4:
                week = 1
            else:
                week = schedule_json['currentWeekNumber']+1
        return schedule(days[days.index(message_parameter)], week)

    # на всю неделю
    elif message_parameter == 'на всю неделю':
        x = []
        for day in days:
            x.append(day.capitalize() + ':\n' + schedule(day, schedule_json['currentWeekNumber']) + '\n')
        return '\n'.join(x)
    else:
        return 'Извините, я вас не понимаю'
