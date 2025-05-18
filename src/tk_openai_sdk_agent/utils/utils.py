from typing import TypeVar




from ..error_trace import get_error_detail

from ..message import message
import re

import json

T = TypeVar("T")


def fomart_agent_rsp(rsp: list[dict], ai_model: str) -> list[dict]:
    return [
        {
            "source_ip_query": item["IP称呼"],
            "source_character_query": item["角色名称"],
            "ai_rsp": {ai_model: item["IP官方名称"]},
        }
        for item in rsp
    ]


def fomart_rsp(rsp: list[dict], ai_model: str) -> list[dict]:
    return [
        {
            "source_ip_query": item["IP称呼"],
            "source_character_query": item["角色名称"],
            "ai_rsp": item["IP官方名称"],
            "ai_model": ai_model,
        }
        for item in rsp
    ]
def fix_json(json_str:str):
    
    # 预处理: 去除第一个[之前的所有字符串
    json_str =  '['+json_str.split('[', 1)[-1]
        
    # 预处理：去除首尾空白字符
    json_str = json_str.strip()
    
    
    
    # 尝试直接解析完整JSON
    try:
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError:
        pass

    # 逆向扫描定位所有可能的闭合点
    stack = []
    candidates = []
    in_string = False  # 字符串状态标识
    escape = False     # 转义字符标识
    
    # 正向扫描记录所有候选闭合点
    for idx, char in enumerate(json_str):
        # 处理字符串状态
        if char == '"' and not escape:
            in_string = not in_string
        escape = char == '\\' and not escape
        
        # 仅处理非字符串内的结构
        if not in_string:
            if char == '{':
                stack.append(idx)
            elif char == '}':
                if stack:
                    stack.pop()
                    # 记录每个可能的闭合点
                    candidates.append(idx)

    # 逆向尝试候选闭合点
    for end_idx in reversed(candidates):
        # 构造候选JSON
        candidate = json_str[:end_idx+1] + ']'
        # 尝试解析
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            continue

    # 保底处理：返回空数组
    return json_str

def fomart_rsp_str(rsp: str):
    
    
    if "json" in rsp:
        try:
            pattern = r"```json\n([\s\S]*?)```"
            result = re.findall(pattern, rsp)[0].strip()
            return result
        except Exception as e:
            message.debug(get_error_detail(e))
    rsp = fix_json(rsp)
    
    return rsp
