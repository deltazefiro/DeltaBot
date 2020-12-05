from .main import *

__plugin_name__ = 'time_planning'
__plugin_usage__ = r"""
目标计划管理插件
Usage:
 - settask [tasks]
    (覆盖)设定目标计划
 - listtask
    显示目标计划列表
 - finishtask [task_idxs]
    完成目标任务
 - addtask [tasks]
    增添目标任务
""".strip()