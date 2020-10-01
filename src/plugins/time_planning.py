from nonebot import on_command, CommandSession
import nonebot
import time
import random
import pickle
import json
import aiofiles
import os

# tasks.json
# {
#   
#   <user1_id>:{
#       "tasks":[
#           {"content":<task>, "time":<time>, "is_finished"=<bool>},
#           {"content":<task>, "time":<time>, "is_finished"=<bool>}
#       ],
#       "finished_tasks_num":<num>
#   },
#
#   <user2_id>:{
#       "tasks":[
#           {"content":<task>, "time":<time>, "is_finished"=<bool>},
#           {"content":<task>, "time":<time>, "is_finished"=<bool>}
#       ],
#       "finished":<num>,
#        "unfinished":<num>
#   }
#
# }

TASKS_DATA_PATH = "../data/tasks.json"
TASKS_DATA_PATH = os.path.join(os.path.dirname(__file__), TASKS_DATA_PATH)

async def process_set_task(task, user_id):
    try:
        with open(TASKS_DATA_PATH, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = {}

    if not user_id in data:
        data[user_id] = {'tasks':[], 'unfinished':0, 'finished':0}

    tasks = [t.strip() for t in task.split()]
    data[user_id]['tasks'] = [{'content':c, 'time':None, 'is_finished':False} for c in tasks]
    data[user_id]['unfinished'] = len(tasks)

    with open(TASKS_DATA_PATH, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


async def process_list_task(user_id):
    try:
        with open(TASKS_DATA_PATH, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = {}

    if not user_id in data:
        return "[UserID %s] 尚未创建任务" %user_id
    
    ret = "[UserID %s]\n未完成任务%d项， 已完成任务%d项\n" % (user_id, data[user_id]['unfinished'], data[user_id]['finished'])

    tasks = data[user_id]['tasks']
    for idx in range(len(tasks)):
        t = tasks[idx]
        content, time, is_finished = t['content'], t['time'], t['is_finished']

        time = " ⏳" if  time and not is_finished else ""
        is_finished = "◆" if  is_finished  else "◇"

        ret = ret + f"{is_finished}{idx+1}. {content}{time}\n"
    
    return ret


async def process_finish_task(task_idx, user_id):
    try:
        with open(TASKS_DATA_PATH, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = {}

    if not user_id in data:
        return "[UserID %s] 尚未创建任务" %user_id

    try:
        if not data[user_id]['tasks'][task_idx-1]['is_finished']:
            data[user_id]['tasks'][task_idx-1]['is_finished'] = True
            data[user_id]['unfinished'] -= 1
            data[user_id]['finished'] += 1
    except IndexError:
        return False

    with open(TASKS_DATA_PATH, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    return data[user_id]['unfinished'], data[user_id]['finished']


@on_command('settask', aliases=('setplan', 'settasks', 'task'))
async def set_task(session: CommandSession):
    user_id = str(session.event.user_id)
    task = session.get('task', prompt="[UserID %s] 请输入目标计划，一行一个目标，不需加序号" %user_id)
    print("Log: %s" %task)
    await process_set_task(task, user_id)
    await session.send("目标设定成功")

@set_task.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['task'] = stripped_arg
    elif not session.is_first_run:
        session.pause('Input invalid. Please input again.')


@on_command('listtask', aliases=('showtask', 'listtasks'))
async def list_task(session: CommandSession):
    user_id = str(session.event.user_id)
    await session.send(await process_list_task(user_id))


@on_command('finishtask', aliases=('finishplan'))
async def finish_task(session: CommandSession):
    user_id = str(session.event.user_id)
    task_idx = int(session.get('task_idx', prompt="[UserID %s] 请输入完成的目标序号" %user_id))
    ret = await process_finish_task(task_idx, user_id)
    if ret:
        await session.send("登记完成成功！目前未完成%d项，已完成%d项" %ret)
    else:
        await session.send("登记完成失败，请检查输入是否有效")

@finish_task.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['task_idx'] = stripped_arg
    elif not session.is_first_run:
        session.pause('Input invalid. Please input again.')