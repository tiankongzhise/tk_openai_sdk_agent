from pydantic import BaseModel,field_validator,Field
from typing import Any,Generator
from copy import deepcopy

from ...message import message

import re 
import unicodedata
import math

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
        
        
    # 步骤 2：使用预生成的转换表快速删除控制字符（性能优化）
    value = value.translate(CONTROL_CHARS_TRANSLATION_TABLE)
    
        
    # 步骤 3: 将中文的：替换为英文的:
    value = value.replace('：', ':')
    
    # 步骤 4：过滤非保留符号（仅保留有效字符）
    value = re.sub(r'[^\w\s\u4e00-\u9fa5·\-\:\']', ' ', value)
    
    
    # 步骤 5：替换非空格空白符为空格，并合并连续空格
    value = re.sub(r'[\t\n\r\v\f]', ' ', value)  # 非空格空白符 → 空格
    value = re.sub(r' +', ' ', value)  # 合并连续空格为单个空格
    
    # 步骤 6：去除首尾空字符（此时空字符均为空格）
    value = value.strip()
    
 

    
    # 步骤 7：清理非空格分隔符（·、-）周围的空字符
    value = re.sub(r'\s*([·\-\:\'])\s*', r'\1', value)
    
    # 步骤 8：去重连续的非空符号（如 --- 或 ··· 保留一个）
    value = re.sub(r'([^\w\s\u4e00-\u9fa5])\1+', r'\1', value)
    
    # 步骤 9：将全部字符小写
    value = value.lower()
    
    # 步骤10: 移除前后的空格
    value = value.strip()
    
    # 步骤 11：若存在变动,则在debug时输出提示
    if temp_value != value:
        message.debug(f"{cls}存在变动{temp_value} -> {value}")
        
        
    return value


class MinxIn(object):
    __mixin__ = True
    
    @field_validator('ip', 'character', mode='before',check_fields=False)
    def preprocess_input(cls, value) -> str:
        return process_input(cls,value)



 

class BaseSourceData(BaseModel,MinxIn):
    ip:str
    character:str
    

class BaseResponse(BaseModel,MinxIn):
    ip:str
    character:str
    ai_rsp:str
    ai_model:str
    
    @field_validator('ai_rsp',mode='before')
    def ai_rsp_preprocess(cls,value) -> str:
        return process_input(cls,value)

class BaseDTO(BaseModel):
    status: str
    data:list[BaseResponse] = Field(default_factory=list)
    message: str
    extra_info:dict = Field(default_factory=dict)
    fail_data:str = Field(default="")


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


class LLMResponseData(BaseResponse):
    ip:str = Field(...,alias="IP称呼")
    character:str = Field(...,alias="角色名称")
    ai_rsp:str = Field(...,alias="IP官方名称")


class LLMResponseDTO(BaseDTO):
    data:list[LLMResponseData] = Field(default_factory=list)
    
class VerifySourceData(BaseModel):
    ip:str = Field(...,alias="IP")
    character:str = Field(...,alias="角色")
    deepseek_r1:str = Field(...,alias="DEEPSEEK-R1")
    doubao_pro_32k:str = Field(...,alias="DOUBAO-PRO-32K")
    doubao_thinking_pro:str = Field(...,alias="DOUBAO-THINKING-PRO")
    doubao_vision_pro:str = Field(...,alias="DOUBAO-VISION-PRO")
    @field_validator("deepseek_r1","doubao_pro_32k","doubao_thinking_pro","doubao_vision_pro",mode="before")
    def process_data(cls,value)->str:
        if value is None:
            return "未知"
        if  isinstance(value, float) and math.isnan(value):
            return "未知"
        if isinstance(value, str):
            return value
        return str(value)

class PreVerifyDTO(BaseDTO):
    data:list[VerifySourceData]
    toml_config:dict
    
class DuplicateVerifyDTO(BaseDTO):
    data:list[VerifySourceData]
    toml_config:dict

class MultiLLMVerifyData(BaseResponse):
    ip:str = Field(...,alias="IP称呼")
    character:str = Field(...,alias="角色名称")
    ai_rsp:str = Field(...,alias="验证结果")
    confidence_level:str = Field(...,alias="置信度")
    basis:list[str] = Field(default_factory=list,alias="依据")

class MultiLLMVerifyDTO(BaseDTO):
    data:list[MultiLLMVerifyData] = Field(default_factory=list)

