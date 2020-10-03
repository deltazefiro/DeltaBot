import json
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

TASKS_DATA_PATH = "./data/tasks.json"
TASKS_DATA_PATH = os.path.join(os.path.dirname(__file__), TASKS_DATA_PATH)

def process_set_task(task, user_id):
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


def process_list_task(user_id):
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


def process_finish_task(task_idx, user_id):
    try:
        with open(TASKS_DATA_PATH, mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = {}

    user_id = str(user_id)
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


def process_add_task(task: str, user_id: int):
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


process_set_task("hahahah\nasdfadsf\nasdf", '10000')
print(process_list_task('10000'))
# process_finish_task(4, '10000')
process_add_task("haha\nasdfsdf", '10000')
print(process_list_task('10000'))