from nonebot import on_command, CommandSession, message

__plugin_name__ = 'xml'
__plugin_usage__ = r"""
Transform xml code into a XML card.
*Notice that excessive XML msg may cause your account frozen!*
Command(s):
 - /xml [code]
""".strip()

def get_xml_segment(data: str) -> message.MessageSegment:
    return message.MessageSegment(type_='xml', data={'data': str(data)})

@on_command('xml', aliases=('toxml', 'to_xml'))
async def xml(session: CommandSession):
    data = session.get('data', prompt="Please input xml data.")
    await session.send(get_xml_segment(data))

@xml.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['data'] = arg
        return

    if not arg:
        session.pause('Please input the xml data.')

    session.state[session.current_key] = arg