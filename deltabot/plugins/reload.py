import sys
from os import path

import nonebot
from loguru import logger
from nonebot import on_command, CommandSession, permission, get_bot

from .. import config

__plugin_name__ = '[A]reload'
__plugin_usage__ = r"""
重载配置文件和所有插件
【需要管理员权限】
Command(s):
 - /reload
""".strip()

@on_command('reloadplugins', aliases=('reloadplugin', 'reload'), permission=permission.SUPERUSER)
async def reloadplugins(session: CommandSession):
    # Reload config
    get_bot().config = config
    logger.info("Config reloaded.")

    # Reload plugins
    plugins = nonebot.plugin.get_loaded_plugins()
    for plugin in plugins:
        module_path = plugin.module.__name__
        nonebot.plugin.PluginManager.remove_plugin(module_path)
        for module in list(
                filter(lambda x: x.startswith(module_path), sys.modules.keys())):
            del sys.modules[module]

    reloaded_plugins = nonebot.load_plugins(path.dirname(__file__), 'deltabot.plugins')
    logger.info(f"{len(reloaded_plugins)} plugin(s) reloaded.")
    await session.send(f"已成功重载{len(reloaded_plugins)}个插件")

