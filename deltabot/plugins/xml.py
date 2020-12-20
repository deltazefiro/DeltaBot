from nonebot import on_command, CommandSession, message

__plugin_name__ = 'xml'
__plugin_usage__ = r"""
将xml代码转换为卡片
**过度使用有封号风险！**
Command(s):
 - /xml [xml代码]
""".strip()

def get_xml_segment(data: str) -> message.MessageSegment:
    return message.MessageSegment(type_='xml', data={'data': str(data)})

@on_command('xml', aliases=('toxml', 'to_xml'))
async def xml(session: CommandSession):
    data = session.get('data', prompt="请输入xml代码")
    await session.send(get_xml_segment(data))

@xml.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['data'] = arg
        return

    if not arg:
        session.pause('请输入xml代码')

    session.state[session.current_key] = arg