from nonebot import on_command, CommandSession, permission
import nonebot
import os

__plugin_name__ = 'reload'
__plugin_usage__ = r"""
Reload all plugins.
*Required admin permission*
Usage:
 - /reload
""".strip()

PLUGINS_PATH = "."
PLUGINS_PATH = os.path.join(os.path.dirname(__file__), PLUGINS_PATH)

@on_command('reloadplugins', aliases=('reloadplugin', 'reload'), permission=permission.SUPERUSER)
async def reloadplugins(session: CommandSession):
    for f in os.listdir(PLUGINS_PATH):
        if f != '__pycache__' and f != 'reload.py':
            plugin_path = 'plugins.' + os.path.splitext(f)[0]
            ret = nonebot.plugin.reload_plugin(plugin_path)
            if not ret:
                ret = nonebot.plugin.load_plugin(plugin_path)
            if not ret:
                await session.send("[WARNING] Failed to reload '%s' plugin!" %plugin_path)
    await session.send("Plugins reloaded.")



# @on_command('reloadrunningplugins', aliases=('reloadrplugin', 'reload'))
# async def reload_running_plugins(session: CommandSession):
#     plugins = nonebot.plugin.get_loaded_plugins()
#     for plugin in plugins:
#         plugin_path = plugin.module.__name__
#         # await session.send("Reloading %s ..." %plugin_path)
#         if plugin_path != 'plugin.reload':
#             nonebot.plugin.reload_plugin(plugin_path)
#     await session.send("Reloaded %d plugins successfully." %(len(plugins)-1))
