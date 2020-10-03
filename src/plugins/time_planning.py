from nonebot import on_command, CommandSession
import nonebot
import time
import random
import pickle
import json
import aiofiles
import os
import re

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

async def process_set_task(task: str, user_id: int):
    try:
        with open(TASKS_DATA_PATH, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = {}

    user_id = str(user_id)
    if not user_id in data:
        data[user_id] = {'tasks':[], 'unfinished':0, 'finished':0}

    tasks = [t.strip() for t in task.split()]
    data[user_id]['tasks'] = [{'content':c, 'time':None, 'is_finished':False} for c in tasks]
    data[user_id]['unfinished'] = len(tasks)
    data[user_id]['finished'] = 0

    with open(TASKS_DATA_PATH, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


async def process_list_task(user_id: int):
    try:
        with open(TASKS_DATA_PATH, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = {}

    user_id = str(user_id)
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


async def process_finish_task(task_idxs: str, user_id: int) -> bool:
    try:
        with open(TASKS_DATA_PATH, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = {}

    user_id = str(user_id)

    if not user_id in data:
        return "[UserID %s] 尚未创建任务" %user_id

    try:
        task_idxs = [int(i) for i in re.split(',|，', task_idxs)]
    except TypeError:
        return False
    if max(task_idxs) > len(data[user_id]['tasks']) or min(task_idxs) <= 0:
        return False

    for  i in task_idxs:
        if not data[user_id]['tasks'][i-1]['is_finished']:
            data[user_id]['tasks'][i-1]['is_finished'] = True
            data[user_id]['unfinished'] -= 1
            data[user_id]['finished'] += 1

    with open(TASKS_DATA_PATH, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return True


async def process_add_task(task: str, user_id: int):
    try:
        with open(TASKS_DATA_PATH, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = {}

    user_id = str(user_id)
    if not user_id in data:
        data[user_id] = {'tasks':[], 'unfinished':0, 'finished':0}

    tasks = [t.strip() for t in task.split()]
    data[user_id]['tasks'].extend([{'content':c, 'time':None, 'is_finished':False} for c in tasks])
    data[user_id]['unfinished'] += len(tasks)

    with open(TASKS_DATA_PATH, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)



@on_command('settask', aliases=('setplan', 'settasks', 'task', 'taskset'))
async def set_task(session: CommandSession):
    user_id = session.event.user_id
    task = session.get('task', prompt="[UserID %s] 请输入目标计划，一行一个目标，不需加序号" %user_id)
    print("Log: %s" %task)
    await process_set_task(task, user_id)
    ret = await process_list_task(user_id)
    await session.send("目标设定成功!\n%s" %ret)

@set_task.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['task'] = stripped_arg
    elif not session.is_first_run:
        session.pause('Input invalid. Please input again.')


@on_command('listtask', aliases=('showtask', 'listtasks', 'tasklist'))
async def list_task(session: CommandSession):
    user_id = session.event.user_id
    await session.send(await process_list_task(user_id))


@on_command('finishtask', aliases=('finishplan', 'taskfinish'))
async def finish_task(session: CommandSession):
    user_id = session.event.user_id
    task_idxs = session.get('task_idxs', prompt="[UserID %s] 请输入完成的目标序号(多个已完成可逗号隔开序号)" %user_id)
    ret = await process_finish_task(task_idxs, user_id)
    if ret:
        await session.send("登记完成成功！\n%s" %await process_list_task(user_id))
    else:
        await session.send("登记完成失败，请检查输入是否有效")

@finish_task.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['task_idxs'] = stripped_arg
    elif not session.is_first_run:
        session.pause('Input invalid. Please input again.')


@on_command('addtask', aliases=('taskadd'))
async def add_task(session: CommandSession):
    user_id = session.event.user_id
    task = session.get('task', prompt="[UserID %s] 请输入要添加的计划，一行一个目标，不需加序号" %user_id)
    await process_add_task(task, user_id)
    ret = await process_list_task(user_id)
    await session.send("目标设定成功!\n%s" %ret)

@add_task.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['task'] = stripped_arg
    elif not session.is_first_run:
        session.pause('Input invalid. Please input again.')