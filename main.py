# # session.current_arg_text
# # session.state['mode'] = 'default'
# # 代码级教学：SoreHait

# from nonebot import on_command, CommandSession
# from hoshino.modules.DJMAX_HoshinoBot.deps.djmax_bests_generate.djmax_bests import generate
# from hoshino.config import RES_DIR
# from hoshino import R
# import os


# imgpath = os.path.join(os.path.expanduser(RES_DIR), 'img', 'djmax')

# @on_command('djmax', only_to_me=False)
# async def djmax(session: CommandSession):
#     get_id = session.get('id')
#     get_keys = session.get('keys')
#     img = await generate.generate_bests(get_id, get_keys)
#     img.save(os.path.join(imgpath, f"{get_id}_{get_keys}b_b100.png"))
#     img_cqcode = R.img(f"djmax/{get_id}_{get_keys}b_b100.png").cqcode
#     await session.send(img_cqcode)

    
# @djmax.args_parser
# async def _(session: CommandSession):
#     data = session.current_arg_text.split()
#     session.state['id'] = data[0]
#     session.state['keys'] = data[1]
#     return

from nonebot import on_command, CommandSession
from hoshino.modules.DJMAX_HoshinoBot.deps.djmax_bests_generate.djmax_bests import generate
from hoshino.config import RES_DIR
from hoshino import R
import os
import json

# --- 配置部分 ---
# 数据文件路径
DATA_PATH = os.path.join(os.path.dirname(__file__), 'djmax_bind_data.json')
imgpath = os.path.join(os.path.expanduser(RES_DIR), 'img', 'djmax')

# --- 读写 JSON 工具函数 ---
def _load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def _save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- 绑定指令 ---
@on_command('djmax_bind', only_to_me=False)
async def djmax_bind(session: CommandSession):
    qq = str(session.ctx['user_id'])
    djmax_id = session.current_arg_text.strip()
    
    if not djmax_id:
        await session.send('格式错误，请使用：djmax_bind [你的ID]')
        return

    data = _load_data()
    data[qq] = djmax_id
    _save_data(data)
    
    await session.send(f'绑定成功！QQ: {qq} -> ID: {djmax_id}')

# --- 解绑指令 ---
@on_command('djmax_unbind', only_to_me=False)
async def djmax_unbind(session: CommandSession):
    qq = str(session.ctx['user_id'])
    data = _load_data()
    
    if qq in data:
        del data[qq]
        _save_data(data)
        await session.send('解绑成功！')
    else:
        await session.send('你还没有绑定ID。')

# --- 主指令 (基于第一版逻辑) ---
@on_command('djmax', only_to_me=False)
async def djmax(session: CommandSession):
    # 1. 获取参数 (完全沿用第一版逻辑)
    get_id = session.get('id')
    get_keys = session.get('keys')
    
    # 2. 生成图片
    try:
        img = await generate.generate_bests(get_id, get_keys)
        
        # 确保目录存在
        if not os.path.exists(imgpath):
            os.makedirs(imgpath)
            
        # 保存文件
        file_name = f"{get_id}_{get_keys}b_b100.png"
        img.save(os.path.join(imgpath, file_name))
        
        # 发送图片 (修正了文件名路径)
        img_cqcode = R.img(f"djmax/{file_name}").cqcode
        await session.send(img_cqcode)
        
        # 3. 自动绑定逻辑 (可选)：如果出图成功，顺便把ID绑定给当前用户
        qq = str(session.ctx['user_id'])
        data = _load_data()
        if data.get(qq) != get_id: # 只有当绑定的ID不一致时才更新
            data[qq] = get_id
            _save_data(data)
            # 这里不发送提示，避免刷屏，静默绑定
            
    except Exception as e:
        await session.send(f'❌ 出图失败：{e}')

# --- 参数解析器 (沿用第一版，增加绑定ID注入) ---
@djmax.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()
    
    # 情况A: 用户输入了参数 (例如 "Amamiya_Akina 4") -> 优先使用输入
    if len(args) >= 2:
        session.state['id'] = args[0]
        session.state['keys'] = args[1]
    
    # 情况B: 用户只输入了键数 (例如 "4") -> 尝试读取绑定
    elif len(args) == 1:
        arg1 = args[0]
        if arg1 in ['4', '5', '6', '8']:
            qq = str(session.ctx['user_id'])
            data = _load_data()
            bind_id = data.get(qq)
            
            if bind_id:
                session.state['id'] = bind_id
                session.state['keys'] = arg1
            else:
                await session.send('❌ 未检测到绑定ID，请手动输入ID或使用 [djmax绑定] 指令。')
                # 终止后续执行
                session.state['id'] = None 
        else:
             await session.send('❌ 参数错误，键数必须是 4/5/6/8。')
             session.state['id'] = None
    else:
        # 没输入任何内容
        await session.send('❌ 请输入 ID 和 键数，例如：djmax Amamiya_Akina 4')
        session.state['id'] = None

    return
