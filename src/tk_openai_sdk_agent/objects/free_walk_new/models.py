from pydantic import BaseModel,field_validator
from typing import Any,Generator
from copy import deepcopy

from ...message import message

import re 
import unicodedata

# 预生成 Unicode 控制字符的转换表（仅生成一次）
def _generate_control_chars_translation_table():
    """生成控制字符的转换表（键：控制字符的 Unicode 码点，值：None）"""
    control_chars = set()
    # Unicode 码点范围：0 到 0x10FFFF（基本多文种平面 + 辅助平面）
    for code_point in range(0x110000):
        char = chr(code_point)
        if unicodedata.category(char).startswith('C'):
            control_chars.add(code_point)
    # 转换表：控制字符的码点 → None（删除）
    return str.maketrans({cp: None for cp in control_chars})

# 全局缓存转换表（程序启动时生成一次）
CONTROL_CHARS_TRANSLATION_TABLE = _generate_control_chars_translation_table()

def process_input(cls, value) -> str:
    temp_value = deepcopy(value)
    # 步骤 1：确保输入为字符串（兼容非字符串输入）
    if not isinstance(value, str):
        if value is None:
            raise ValueError("输入不能为 None")
        value = str(value)  # 非字符串类型转为字符串（如数字）
    
    # 步骤 2：替换非空格空白符为空格，并合并连续空格
    value = re.sub(r'[\t\n\r\v\f]', ' ', value)  # 非空格空白符 → 空格
    value = re.sub(r' +', ' ', value)  # 合并连续空格为单个空格
    
    # 步骤 3：去除首尾空字符（此时空字符均为空格）
    value = value.strip()
    
    # 步骤 4：使用预生成的转换表快速删除控制字符（性能优化）
    value = value.translate(CONTROL_CHARS_TRANSLATION_TABLE)
    
    # 步骤 5: 将中文的：替换为英文的:
    value = value.replace('：', ':')
    
    # 步骤 6：过滤非保留符号（仅保留有效字符）
    value = re.sub(r'[^\w\s\u4e00-\u9fa5·\-\:\']', ' ', value)
    
    # 步骤 7：清理非空格分隔符（·、-）周围的空字符
    value = re.sub(r'\s*([·\-\:\'])\s*', r'\1', value)
    
    # 步骤 8：去重连续的非空符号（如 --- 或 ··· 保留一个）
    value = re.sub(r'([^\w\s\u4e00-\u9fa5])\1+', r'\1', value)
    
    # 步骤 9：将全部字符小写
    value = value.lower()
    
    # 步骤 10：若存在变动,则在debug时输出提示
    if temp_value != value:
        message.debug(f"{cls}存在变动{temp_value} -> {value}")
    return value


class MinxIn(object):
    __mixin__ = True
    
    @field_validator('ip', 'character', mode='before',check_fields=False)
    def preprocess_input(cls, value) -> str:
        return process_input(cls,value)


class BaseResponse(BaseModel,MinxIn):
    ip:str
    character:str
    ai_rsp:str
    
    @field_validator('ai_rsp',mode='before')
    def ai_rsp_preprocess(cls,value) -> str:
        return process_input(cls,value)
 

class BaseSourceData(BaseModel,MinxIn):
    ip:str
    character:str
    



class BaseDTO(BaseModel):
    status: str
    data:list[Any]
    message: str
    extra_info:dict


class FreeWalkSourceData(BaseSourceData):
    ...

class FreeWalkSourceDTO(BaseDTO):
    data:Generator[FreeWalkSourceData,Any,None]

class PreWorkDTO(BaseDTO):
    data:list[FreeWalkSourceData]
    toml_config:dict



class DuplicateDTO(BaseDTO):
    data:list[FreeWalkSourceData]
    toml_config:dict
