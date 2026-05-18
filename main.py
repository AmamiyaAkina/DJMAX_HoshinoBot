from nonebot import on_command, CommandSession
# 导入两个核心的出图函数
from hoshino.modules.DJMAX_HoshinoBot.deps.djmax_bests_generate.djmax_bests import generate
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

# --- 智能参数解析器 ---
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

    # ---------------------------------------------------------
    # 2. 核心业务指令解析
    # ---------------------------------------------------------
    
    get_id = None
    get_keys = None
    target_action = None

    # 步骤 A: 提取开头的 ID (如果存在且不是关键词)
    start_idx = 0
    if first_word not in [CMD_BESTS, CMD_LIST]:
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
        
        # 提取 list 后面的剩余参数 (用于解析 sc 和 level)
        remaining_args = args[next_idx:]
        if not remaining_args:
            await session.send('❌ 分表查询缺少等级参数。例如：djmax list 4 15 或 djmax list 4 sc15')
            session.state['action'] = None
            return

        is_sc = False # 【默认改为 False (Normal)】
        level = 0
        # 将剩余部分拼起来方便正则匹配（处理 sc 15 分开写的情况）
        combined_str = "".join(remaining_args) 

        # 【核心修改】新的正则逻辑：
        # ^(?:sc)?(\d+)$ 
        # 解释：^ 开头， (?:sc)? 表示 "sc" 是可选的（有或没有）， (\d+) 捕获结尾的数字作为等级
        match = re.match(r'^(?:sc)?(\d+)$', combined_str, re.IGNORECASE)
        
        if match:
            level = int(match.group(1))
            # 检查原始拼接字符串里是否包含 'sc'，如果有则设为 True，否则保持默认的 False
            if re.search(r'^sc', combined_str, re.IGNORECASE):
                is_sc = True
        else:
            await session.send('❌ 分表等级格式错误。请使用类似 15, sc15, SC 15 的格式。')
            session.state['action'] = None
            return

        # 存入 state
        session.state['get_id'] = get_id
        session.state['get_keys'] = get_keys
        session.state['is_sc'] = is_sc
        session.state['level'] = level

    else:
        await session.send(f'❌ 未知的指令关键词 `{keyword}`。目前支持: b100, list')
        target_action = None

    session.state['action'] = target_action
    return
