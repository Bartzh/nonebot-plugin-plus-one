import random

from nonebot.plugin import on_message
from nonebot.adapters import Event, Message, Bot
from nonebot_plugin_session import extract_session, SessionIdType

from nonebot.adapters.onebot.v11 import GroupMessageEvent

from .config import config

plus = on_message(priority=config.plus_one_priority, block=False)
#msg_dict = {}
group_dict = {}


def is_equal(msg1: Message, msg2: Message):
    """判断是否相等"""
    if len(msg1) == len(msg2) == 1 and msg1[0].type == msg2[0].type == "image":
        if msg1[0].data["file_size"] == msg2[0].data["file_size"]:
            return True
    if msg1 == msg2:
        return True


@plus.handle()
async def plush_handler(bot: Bot, event: GroupMessageEvent):
#    global msg_dict
    global group_dict

    session = extract_session(bot, event)
    group_id = session.get_id(SessionIdType.GROUP).split("_")[-1]
    if group_id not in config.plus_one_white_list:
        return

    # 获取群聊记录
#    text_list = msg_dict.get(group_id, None)
#    if not text_list:
#        text_list = []
#        msg_dict[group_id] = text_list

    # 获取当前信息
    msg = event.get_message()

    if group_id not in group_dict:
        group_dict[group_id] = {"last_msg":"","repeat_times":0,"random_time":9}
    if is_equal(group_dict[group_id]["last_msg"], msg):
        group_dict[group_id]["repeat_times"] += 1
    else:
        group_dict[group_id]["repeat_times"] = 0
    group_dict[group_id]["last_msg"] = msg
    if group_dict[group_id]["repeat_times"] == 1:
        gourp_dict[group_id]["random_time"] = random.randint(1, 3)
    if group_dict[group_id]["repeat_times"] == group_dict[group_id]["random_time"]:
        await plus.send(msg)

#    try:
#        if not is_equal(text_list[-1], msg):
#            text_list = []
#            msg_dict[group_id] = text_list
#    except IndexError:
#        pass

#    text_list.append(msg)

#    if len(text_list) > 1:
#        await plus.send(msg)
