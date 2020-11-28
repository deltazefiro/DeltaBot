from nonebot import on_command, CommandSession
from .task_process import *


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


@on_command('addtask', aliases='taskadd')
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