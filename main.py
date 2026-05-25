from nonebot import on_command, CommandSession
# 导入两个核心的出图函数
from hoshino.modules.DJMAX_HoshinoBot.deps.djmax_bests_generate.djmax_bests import generate
from hoshino.modules.DJMAX_HoshinoBot.deps.djmax_bests_generate.djmax_bests import api_handler
from hoshino.config import RES_DIR
from hoshino import R
import os
import json
import re # 引入正则表达式模块，用于解析 sc15 这种格式

# --- 🛠️ 配置与常量定义 ---
DATA_PATH = os.path.join(os.path.dirname(__file__), 'djmax_bind_data.json')
imgpath = os.path.join(os.path.expanduser(RES_DIR), 'img', 'djmax')

CMD_BIND = 'bind'
CMD_UNBIND = 'unbind'
CMD_BESTS = 'b100'   # 修改：B100 现在作为明确的功能关键词
CMD_LIST = 'list'    # 新增：分表查询的功能关键词
CMD_PACK = 'pack'
CMD_LISTDLC = 'listdlc'

VALID_BMODES = [4, 5, 6, 8]

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

# --- 子功能实现区 (便于后续维护扩展) ---

# 1. 绑定ID功能
async def handle_bind(session: CommandSession, args: list):
    qq = str(session.ctx['user_id'])
    # bind后面的参数就是ID
    djmax_id = args[1] if len(args) > 1 else ""
    
    if not djmax_id:
        await session.send('❌ 格式错误，请使用：djmax bind [你的ID]')
        return

    data = _load_data()
    data[qq] = djmax_id
    _save_data(data)
    await session.send(f'✅ 绑定成功！QQ: {qq} -> ID: {djmax_id}')

# 2. 解绑ID功能
async def handle_unbind(session: CommandSession):
    qq = str(session.ctx['user_id'])
    data = _load_data()
    
    if qq in data:
        del data[qq]
        _save_data(data)
        await session.send('✅ 解绑成功！')
    else:
        await session.send('❌ 你还没有绑定任何ID。')

# 3. Bests (B100) 出图功能
async def generate_bests(session: CommandSession, get_id: str, get_keys: int):
    try:
        img = await generate.generate_bests(get_id, get_keys)
        
        if not os.path.exists(imgpath):
            os.makedirs(imgpath)
            
        file_name = f"{get_id}_{get_keys}b_b100.png"
        img.save(os.path.join(imgpath, file_name))
        
        img_cqcode = R.img(f"djmax/{file_name}").cqcode
        await session.send(img_cqcode)
        
        # 出图成功后静默自动绑定
        qq = str(session.ctx['user_id'])
        data = _load_data()
        if data.get(qq) != get_id:
            data[qq] = get_id
            _save_data(data)
            
    except Exception as e:
        error_msg = str(e)
        if "ConnectTimeout" in error_msg or "Connection" in error_msg:
            await session.send("❌ **连接超时**：无法连接到 DJMAX 服务器，请检查网络或稍后再试。")
        else:
            await session.send(f"❌ 出图失败：{error_msg}")

# 4. 指定难度分表
async def generate_scorelist(session: CommandSession, get_id: str, get_keys: int, is_sc: bool, level: int):
    try:
        # 将参数传入底层函数
        img = await generate.generate_scorelist(get_id, get_keys, is_sc, level)
        
        if not os.path.exists(imgpath):
            os.makedirs(imgpath)
            
        # 生成文件名，带上 sc和等级标识
        mode_str = "sc" if is_sc else ""
        file_name = f"{get_id}_{get_keys}k_{mode_str}{level}_list.png"
        img.save(os.path.join(imgpath, file_name))
        
        img_cqcode = R.img(f"djmax/{file_name}").cqcode
        await session.send(img_cqcode)
        
    except Exception as e:
        error_msg = str(e)
        if "ConnectTimeout" in error_msg or "Connection" in error_msg:
            await session.send("❌ **连接超时**：无法连接到 DJMAX 服务器，请检查网络或稍后再试。")
        else:
            await session.send(f"❌ 出图失败：{error_msg}")

# 5. 指定曲包分表
async def generate_scorelist_pack(session: CommandSession, get_id: str, get_keys: int, get_diff:str ,get_pack: str):
    try:
        img = await generate.generate_scorelist_pack(get_id, get_keys, get_diff, get_pack)
        if not os.path.exists(imgpath):
            os.makedirs(imgpath)

        file_name = f"{get_id}_{get_keys}k_{get_diff}_{get_pack}.png"
        img.save(os.path.join(imgpath, file_name))

        img_cqcode = R.img(f"djmax/{file_name}").cqcode
        await session.send(img_cqcode)



    except Exception as e:
        error_msg = str(e)
        if "ConnectTimeout" in error_msg or "Connection" in error_msg:
            await session.send("❌ **连接超时**：无法连接到 DJMAX 服务器，请检查网络或稍后再试。")
        else:
            await session.send(f"❌ 出图失败：{error_msg}")

# 6. 发送全部曲包列表
async def send_dlc_list(session: CommandSession):
    try:
        dlc_list = await api_handler.fetch_dlc_list()
        dlcs = list(getattr(dlc_list, 'root', dlc_list))

        if not dlcs:
            await session.send('❌ 当前没有可用的曲包列表。')
            return

        lines = [f'{dlc.dlcCode}:{dlc.dlcName}' for dlc in dlcs]
        await session.send('\n'.join(lines))
    except Exception as e:
        await session.send(f'❌ 获取曲包列表失败：{e}')

# --- 主指令 ---
@on_command('djmax', only_to_me=False)
async def djmax(session: CommandSession):
    # 从 state 中获取解析好的意图和数据
    action = session.state.get('action')
    
    if action == 'bind':
        await handle_bind(session, 
                          session.state.get('raw_args'))
    elif action == 'unbind':
        await handle_unbind(session)
    elif action == 'b100':
        await generate_bests(session, 
                             session.state.get('get_id'), 
                             session.state.get('get_keys'))
    elif action == 'list':
        await generate_scorelist(session, 
                                 session.state.get('get_id'), 
                                 session.state.get('get_keys'), 
                                 session.state.get('is_sc'), 
                                 session.state.get('level'))
    elif action == 'pack':
        await generate_scorelist_pack(session,
                                      session.state.get('get_id'),
                                      session.state.get('get_keys'),
                                      session.state.get('get_diff'),
                                      session.state.get('get_pack')
        )
    elif action == CMD_LISTDLC:
        await send_dlc_list(session)

# --- 智能参数解析器 ---
# --- 🧠 智能参数解析器 (已修复 pack 指令及 ID 识别问题) ---
@djmax.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()
    raw_args = args 
    
    if not args:
        await session.send('❌ 请输入指令。例如：djmax bind [ID] 或 djmax [ID] b100 4')
        session.state['action'] = None
        return

    first_word = args[0].lower()

    # 1. 基础管理指令判断
    if first_word == CMD_BIND:
        session.state['action'] = CMD_BIND
        session.state['raw_args'] = raw_args
        return
    elif first_word == CMD_UNBIND:
        session.state['action'] = CMD_UNBIND
        return
    elif first_word == CMD_LISTDLC:
        session.state['action'] = CMD_LISTDLC
        return

    # ---------------------------------------------------------
    # 2. 核心业务指令解析
    # ---------------------------------------------------------
    
    get_id = None
    get_keys = None
    target_action = None

    # 步骤 A: 提取开头的 ID (如果存在且不是关键词)
    start_idx = 0
    # ⚠️ 修复点1：在这里加上 CMD_PACK，防止 pack 被误判为 ID
    if first_word not in [CMD_BESTS, CMD_LIST, CMD_PACK]:
        get_id = args[0]
        start_idx = 1
    
    # 如果没有识别到 ID，尝试从绑定数据中获取
    if not get_id:
        qq = str(session.ctx['user_id'])
        data = _load_data()
        get_id = data.get(qq)
        if not get_id:
            await session.send('❌ 未检测到绑定ID，请手动输入ID或使用 [djmax bind] 指令。')
            session.state['action'] = None
            return

    # 步骤 B: 提取后续的关键词和键数(bmode)
    if start_idx >= len(args):
        await session.send('❌ 参数不足。查询B100请用: djmax [ID] b100 4；查询分表请用: djmax [ID] list 4 15')
        session.state['action'] = None
        return

    keyword = args[start_idx].lower()
    
    # 校验并提取 get_keys (键数必须在关键词后面)
    next_idx = start_idx + 1
    if next_idx >= len(args):
         await session.send('❌ 缺少谱面键数(4/5/6/8)。')
         session.state['action'] = None
         return
    
    try:
        get_keys = int(args[next_idx])
        if get_keys not in VALID_BMODES:
            raise ValueError
        next_idx += 1 # 移动指针到 get_keys 之后
    except ValueError:
        await session.send('❌ 谱面键数必须是有效的数字 (4/5/6/8)。')
        session.state['action'] = None
        return

    # 步骤 C: 根据关键词分发任务并提取剩余参数
    if keyword == CMD_BESTS:
        target_action = CMD_BESTS
        session.state['get_id'] = get_id
        session.state['get_keys'] = get_keys

    elif keyword == CMD_LIST:
        target_action = CMD_LIST
        
        remaining_args = args[next_idx:]
        if not remaining_args:
            await session.send('❌ 分表查询缺少等级参数。例如：djmax list 4 15 或 djmax list 4 sc15')
            session.state['action'] = None
            return

        is_sc = False
        level = 0
        combined_str = "".join(remaining_args) 

        match = re.match(r'^(?:sc)?(\d+)$', combined_str, re.IGNORECASE)
        
        if match:
            level = int(match.group(1))
            if re.search(r'^sc', combined_str, re.IGNORECASE):
                is_sc = True
        else:
            await session.send('❌ 分表等级格式错误。请使用类似 15, sc15, SC 15 的格式。')
            session.state['action'] = None
            return

        session.state['get_id'] = get_id
        session.state['get_keys'] = get_keys
        session.state['is_sc'] = is_sc
        session.state['level'] = level

    # 将 pack 的逻辑独立出来，不再混在 list 里面
    elif keyword == CMD_PACK:
        target_action = CMD_PACK
        
        remaining_args = args[next_idx:]
        if len(remaining_args) < 2:  # 至少需要难度和曲包名两部分
            await session.send('❌ 曲包查询缺少参数。请使用：djmax [ID] pack 4 SC Platinum / djmax [ID] pack 4 NM Classic / djmax [ID] pack 4 HD PackName / djmax [ID] pack 4 MX PackName')
            session.state['action'] = None
            return

        # 直接取列表的第一项作为难度，剩余所有项拼接作为曲包名（这里输入应为 dlcCode）
        diff_input = remaining_args[0].upper()
        get_pack = " ".join(remaining_args[1:]).strip() # 将剩余部分用空格连接，还原带空格的曲包名（但实际应为 dlcCode）

        # 校验难度前缀，新增支持 HD 与 MX
        if diff_input.startswith("SC"):
            get_diff = "SC"
        elif diff_input.startswith("NM"):
            get_diff = "NM"
        elif diff_input.startswith("HD"):
            get_diff = "HD"
        elif diff_input.startswith("MX"):
            get_diff = "MX"
        else:
            await session.send('❌ 难度格式错误。请使用 SC、NM、HD 或 MX 开头。')
            session.state['action'] = None
            return

        if not get_pack:
            await session.send('❌ 未检测到有效的曲包代码（dlcCode）。')
            session.state['action'] = None
            return

        # 只根据 dlcCode 校验，不使用 dlcName
        try:
            dlc_list = await api_handler.fetch_dlc_list()
            codes = {v.dlcCode.upper() for v in getattr(dlc_list, 'root', dlc_list)}
            if get_pack.upper() not in codes:
                await session.send(f'❌ 未找到曲包代码：{get_pack}（只支持 dlcCode 校验）。')
                session.state['action'] = None
                return
            # 规范化为大写曲包代码
            get_pack = get_pack.upper()
        except Exception:
            await session.send('❌ 无法获取曲包列表，请稍后重试。')
            session.state['action'] = None
            return

        session.state['get_id'] = get_id
        session.state['get_keys'] = get_keys
        session.state['get_diff'] = get_diff
        session.state['get_pack'] = get_pack
        
    else:
        await session.send(f'❌ 未知的指令关键词 `{keyword}`。目前支持: b100, list, pack')
        target_action = None

    session.state['action'] = target_action
    return
