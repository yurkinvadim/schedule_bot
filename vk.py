import vk_api
from schedules.bsuir_schedule import schedule_parameters as bsuir
from schedules.miu_schedule import schedule_parameters as miu
from vk_api.longpoll import VkLongPoll, VkEventType

f = open('token.txt')
token = f.readline()
f.close()
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
universities = ['бгуир', 'миу']
users_universities = {}


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'v': 5.89})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request.lower() in universities:
                university = request.lower()
                users_universities[event.user_id] = university

            if request.lower().startswith('пары'):
                try:
                    if users_universities[event.user_id] == 'бгуир':
                        write_msg(event.user_id, bsuir(request.lower()))
                    elif users_universities[event.user_id] == 'миу':
                        write_msg(event.user_id, miu(request.lower()))
                except KeyError:
                    write_msg(event.user_id, 'Вы не выбрали университет')

