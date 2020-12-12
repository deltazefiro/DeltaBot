# import nonebot
# import time
# from nonebot import on_command, CommandSession, message
#
# __plugin_name__ = 'xml'
# __plugin_usage__ = r"""
# Transform xml code into a xml card.
# Command(s):
#  - /xml [code]
# """.strip()
#
#
# @on_command('xml', aliases=('toxml', 'to_xml'))
# async def xml(session: CommandSession):
#     pass
#
# @xml.args_parser
# async def _(session: CommandSession):
#     arg = session.current_arg
#
#     if session.is_first_run:
#         if arg:
#             session.state['code'] = arg
#         return
#
#     if not arg:
#         session.pause('Please input the xml code.')
#
#     session.state[session.current_key] = arg