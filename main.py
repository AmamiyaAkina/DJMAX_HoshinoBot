# session.current_arg_text
# session.state['mode'] = 'default'
# 代码级教学：SoreHait

from nonebot import on_command, CommandSession
from hoshino.modules.DJMAX_HoshinoBot.djmax_bests_generate.djmax_bests import generate
from hoshino.config import RES_DIR
from hoshino import R
import os


imgpath = os.path.join(os.path.expanduser(RES_DIR), 'img', 'djmax')

@on_command('djmax', only_to_me=False)
async def djmax(session: CommandSession):
    get_id = session.get('id')
    get_keys = session.get('keys')
    img = await generate.generate_bests(get_id, get_keys)
    img.save(os.path.join(imgpath, f"{get_id}.png"))
    img_cqcode = R.img(f"djmax/{get_id}.png").cqcode
    await session.send(img_cqcode)

    

@djmax.args_parser
async def _(session: CommandSession):
    data = session.current_arg_text.split()
    session.state['id'] = data[0]
    session.state['keys'] = data[1]
    return


