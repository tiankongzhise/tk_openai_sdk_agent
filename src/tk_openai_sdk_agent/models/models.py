from pydantic import BaseModel,Field
from typing import Optional


class AiRsp(BaseModel):
    ai_model: str
    ip: str


class IpInfo(BaseModel):
    source_ip_query: str
    source_character_query: str
    ai_rsp: dict

class AgentSetting(BaseModel):
    system_content: str
    prompt: str|None
    ai_model: str 
    ai_model_mapping: dict
    stream: bool 
    print_console: bool
    prompt_template: str
    semaphore_number:int
    
    @classmethod
    def toml_mapping(cls,toml_config:dict):
        return AgentSetting(
            system_content=toml_config.get("SYSTEM_CONTENT"),
            prompt=toml_config.get("PROMPT"),
            ai_model=toml_config.get("AI_MODEL"),
            ai_model_mapping=toml_config.get("AI_MODEL_MAPPING"),
            stream=toml_config.get("STREAM"),
            print_console=toml_config.get("PRINT_CONSOLE"),
            prompt_template=toml_config.get("PROMPT_TEMPLATE"),
            semaphore_number=toml_config.get("SEMAPHORE_NUMBER")
        )

class BaseResponse(BaseModel):
    source_ip_query: str = Field(...,alias="IP称呼")
    source_character_query: str = Field(...,alias="角色名称")
    ai_model: str
    ai_rsp: str = Field(...,alias="IP官方名称")
 
class BaseResult(BaseModel):
    status:str
    message:str
    data:list[BaseResponse] = Field(default_factory=list)
    fail_data:Optional[str] = Field(default=None)

class Response(BaseResponse):
    source_ip_query: str = Field(...,alias="IP称呼")
    source_character_query: str = Field(...,alias="角色名称")
    ai_model: str
    ai_rsp: str = Field(...,alias="IP官方名称")
        
    
class RspResult(BaseResult):
    status:str
    message:str
    data:list[Response] = Field(default_factory=list)
    fail_data:Optional[str] = Field(default=None)

class VerifyResponse(BaseResponse):
    source_ip_query: str = Field(...,alias="IP称呼")
    source_character_query: str = Field(...,alias="角色名称")
    ai_model: str
    ai_rsp: str = Field(...,alias="验证结果")
    confidence_level:str = Field(...,alias="置信度")
    basis:list[str] = Field(...,alias="依据")

class VerifyRspResult(BaseResult):
    status:str
    message:str
    data:list[VerifyResponse] = Field(default_factory=list)
    fail_data:Optional[str] = Field(default=None)
