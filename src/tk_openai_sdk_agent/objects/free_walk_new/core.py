from ...core import SyncAgentWithSdk,AgentWithSdk
from ...utils import fomart_rsp_str
from ...message import message
from ...error_trace import get_error_detail
from .models import DuplicateDTO,FreeWalkSourceData,LLMResponseData,LLMResponseDTO,MultiLLMVerifyData,MultiLLMVerifyDTO,VerifySourceData,DuplicateVerifyDTO

from asyncio import Semaphore
from copy import deepcopy

import json
import pandas as pd

def temp_save(hallucination_data,lost_data):
    from pathlib import Path
    from datetime import datetime
    
    temp_dict = {
        " hallucination_data ":list(hallucination_data),
        " lost_data ":list(lost_data)
    }
    df =pd.DataFrame({k: pd.Series(v) for k, v in temp_dict.items()})
    file_path = Path(__file__).parent / "temp"
    file_path.mkdir(parents=True, exist_ok=True)
    file_name = file_path / f"hallucination_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    if not df.empty:
        df.to_excel(file_name,index=False)

def hallucination_data_statistics(source_data:list[FreeWalkSourceData|VerifySourceData],format_data:list[LLMResponseData|MultiLLMVerifyData]):
    source_data_set = set([f"{i.ip}@{i.character}" for i in source_data])
    format_data_set = set([f"{i.ip}@{i.character}" for i in format_data])
    
    hallucination_data = format_data_set-source_data_set
    lost_data = source_data_set-format_data_set
    
    temp_save(hallucination_data,lost_data)

    
    duplicated_data_count = len(format_data)-len(format_data_set)
    hallucination_data_count = len(hallucination_data)
    lost_data_count = len(lost_data)
    return {
        "duplicated_data_count":duplicated_data_count,
        "hallucination_data_count":hallucination_data_count,
        "lost_data_count":lost_data_count
    }
    
    

class LLMResponseFetcher(AgentWithSdk):
    ...

class MultiLLMResultVerifier(AgentWithSdk):
    ...

class AsyncLLMResponseFetcher(SyncAgentWithSdk):
    def __init__(self,data:DuplicateDTO):
        super().__init__()
        self.init_agent_setting(data.toml_config)
    
    def init_agent_setting(self,toml_config:dict):
        self.set_system_content(toml_config["SYSTEM_CONTENT"])
        self.set_stream(toml_config["STREAM"])
        self.set_print_console(toml_config["PRINT_CONSOLE"])
        self.set_model_mapping(toml_config["AI_MODEL_MAPPING"])
        self.set_ai_model(toml_config["AI_MODEL"])
        self.set_prompt_template(toml_config["PROMPT_TEMPLATE"])
        self.verify_ai_model = toml_config["VERIFY_AI_MODEL"]
    
    def set_prompt(self, query_data:list[FreeWalkSourceData]) -> None:
        temp = deepcopy(self.prompt_template)
        temp_query_data = [f"{query.ip}-{query.character}" for query in query_data]
        temp = temp.replace("{{QUERY_DATA}}", "\n".join(temp_query_data))
        return super().set_prompt(temp)
    
    async def run(self,query_data:list[FreeWalkSourceData],ai_model:str|None = None,semaphore:Semaphore|None=None) -> LLMResponseDTO:
        self.set_prompt(query_data)
        self.semaphore = semaphore
        try:
            if ai_model:
                rsp = await super().run(ai_model=ai_model)
            else:
                rsp = await super().run()
        except Exception as e:
            return LLMResponseDTO(fail_data=f'模型调用失败,错误原因{get_error_detail(e)},调用模型{ai_model},prompt:{self.prompt},',message=get_error_detail(e),status="fail")
        try:
            fomated_rsp_str = fomart_rsp_str(rsp)
            rsp_dict = json.loads(fomated_rsp_str)
            response = []
            if isinstance(rsp_dict,list):
                for item in rsp_dict:
                    try:
                        response.append(LLMResponseData(**{**item,'ai_model':ai_model}))
                    except ValueError as e:
                        message.error(f"item is not a valid Response object:{item},error:{e}")
            elif isinstance(rsp_dict,dict):
                try:
                    response = [LLMResponseData(**{**rsp_dict,'ai_model':ai_model})]
                except ValueError as e:
                    message.error(f"response is not a valid Response object:{rsp_dict},error:{e}")
            else:
                raise ValueError(f"response is not a list or dict:{rsp_dict}")
            temp_count = hallucination_data_statistics(query_data,response)
            message.info(f'{ai_model}-{query_data[0].ip}@{query_data[0].character}到{query_data[-1].ip}@{query_data[-1].character}一共有效{len(response)}条数据'
                         f'重复的回答:{temp_count['duplicated_data_count']},幻觉回答:{temp_count['hallucination_data_count']},丢失询问:{temp_count['lost_data_count']}')
            return LLMResponseDTO(data=response,message="success",status="success")
        except Exception as e:
            return LLMResponseDTO(fail_data=rsp+f'_@#ai_model={ai_model}',message=get_error_detail(e),status="fail")
        

class AsyncMultiLLMResultVerifier(SyncAgentWithSdk):

    def __init__(self,data:DuplicateVerifyDTO):
        super().__init__()
        self.init_agent_setting(data.toml_config)
    
    def init_agent_setting(self,toml_config:dict):
        self.set_system_content(toml_config["VERIFY_SYSTEM_CONTENT"])
        self.set_stream(toml_config["STREAM"])
        self.set_print_console(toml_config["PRINT_CONSOLE"])
        self.set_model_mapping(toml_config["AI_MODEL_MAPPING"])
        self.set_ai_model(toml_config["AI_MODEL"])
        self.set_prompt_template(toml_config["VERIFY_PROMPT_TEMPLATE"])
        self.verify_ai_model = toml_config["VERIFY_AI_MODEL"]
    
    def set_prompt(self, query_data:list[VerifySourceData]) -> None:
        temp = deepcopy(self.prompt_template)
        temp_query_data = [f"{query.ip}@{query.character}@{query.deepseek_r1}@{query.doubao_pro_32k}@{query.doubao_thinking_pro}@{query.doubao_vision_pro}" for query in query_data]
        temp = temp.replace("{{QUERY_DATA}}", "\n".join(temp_query_data))
        return super().set_prompt(temp)
    
    async def run(self,query_data:list[VerifySourceData],ai_model:str|None = None,semaphore:Semaphore|None=None) -> MultiLLMVerifyDTO:
        self.set_prompt(query_data)
        self.semaphore = semaphore
        try:
            if ai_model:
                rsp = await super().run(ai_model=ai_model)
            else:
                rsp = await super().run()
        except Exception as e:
            return MultiLLMVerifyDTO(fail_data=f'模型调用失败,错误原因{get_error_detail(e)},调用模型{ai_model},prompt:{self.prompt},',message=get_error_detail(e),status="fail")
        try:
            fomated_rsp_str = fomart_rsp_str(rsp)
            rsp_dict = json.loads(fomated_rsp_str)
            response = []
            if isinstance(rsp_dict,list):
                for item in rsp_dict:
                    try:
                        response.append(MultiLLMVerifyData(**{**item,'ai_model':ai_model}))
                    except ValueError as e:
                        message.error(f"item is not a valid Response object:{item},error:{e}")
            elif isinstance(rsp_dict,dict):
                try:
                    response = [MultiLLMVerifyData(**{**rsp_dict,'ai_model':ai_model})]
                except ValueError as e:
                    message.error(f"response is not a valid Response object:{rsp_dict},error:{e}")
            else:
                raise ValueError(f"response is not a list or dict:{rsp_dict}")
            temp_count = hallucination_data_statistics(query_data,response)
            message.info(f'{ai_model}-{query_data[0].ip}@{query_data[0].character}到{query_data[-1].ip}@{query_data[-1].character}一共有效{len(response)}条数据'
                         f'重复的回答:{temp_count['duplicated_data_count']},幻觉回答:{temp_count['hallucination_data_count']},丢失询问:{temp_count['lost_data_count']}')
            return MultiLLMVerifyDTO(data=response,message="success",status="success")
        except Exception as e:
            return MultiLLMVerifyDTO(fail_data=rsp+f'_@#ai_model={ai_model}',message=get_error_detail(e),status="fail")
