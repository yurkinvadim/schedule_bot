import vk_api
from schedules.bsuir_schedule import schedule_parameters as bsuir
from schedules.miu_schedule import schedule_parameters as miu

from vk_api.longpoll import VkLongPoll, VkEventType
d
token = "7475007a6ea3354a2c967e11edd1b3775bb49d2f7d3fcb959a5a61d8c3bc50e9dc49c025a3822a450774c"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
universities = ['бгуир', 'миу']
university = ''


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'v': 5.89})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request in universities:
                university = request
            if request.lower().startswith('пары'):
                    if university == 'бгуир':
                            write_msg(event.user_id, bsuir(request.lower()))
                    elif university == 'миу':
                        write_msg(event.user_id, miu())
                    else:
                        write_msg(event.user_id, 'Вы не выбрали университет')

