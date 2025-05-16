from pydantic import BaseModel,Field,validator
from pathlib import Path
from tk_base_utils import get_abs_file_path
from tk_base_utils.file import get_abs_dir_path


class AiPromptConfig(BaseModel):
    """
    
    params:
    
        system_content: str,系统提示词
        prompt_template: str,提示词模板
        placeholder: str,提示词占位符
    """
    system_content:str
    prompt_template:str
    placeholder:str

class AiModelConfig(BaseModel):
    """
    
    AI模型配置
    
    params:
        default_model: str,默认模型
        model_list: list[str],模型列表,默认为空
        verify_model: str,验证模型,默认为空
        model_id_mapping: dict[str,str],模型id映射表
        stream: bool,是否流式返回,默认为False
        print_console: bool,是否打印控制台,默认为False
        max_concurrency: int,最大并发数,默认为100
        prompt_config: AiPromptConfig,提示词配置
        verify_prompt_config: AiPromptConfig,验证提示词配置
    """
    default_model:str
    model_list:list[str] = Field(default_factory=list)
    verify_model:str = ""
    model_id_mapping:dict[str,str]
    stream:bool = False
    print_console:bool = False
    max_concurrency:int = 100
    prompt_config:AiPromptConfig
    verify_prompt_config:AiPromptConfig
    
class FileConfig(BaseModel):
    """
    
    文件配置
    
    params:
        source_data_file_path从文件读入原始数据的路径,输入为str或者Path,结果为Path类型,.开头为当前目录,以$开头为相对路径,如果开头没有.或者$,默认为.
        source_data_dir_path:Path,从文件夹读入原始数据的路径,输入为str或者Path,结果为Path类型,.开头为当前目录,以$开头为相对路径,如果开头没有.或者$,默认为.
        verify_data_file_path:Path,从文件读入验证数据路径,输入为str或者Path,结果为Path类型,.开头为当前目录,以$开头为相对路径,如果开头没有.或者$,默认为.
        verify_data_dir_path:Path,从文件夹读入验证数据路径,输入为str或者Path,结果为Path类型,.开头为当前目录,以$开头为相对路径,如果开头没有.或者$,默认为.
        success_response_file_path:Path,成功的返回值写入的文件路径,输入为str或者Path,结果为Path类型,.开头为当前目录,以$开头为相对路径,如果开头没有.或者$,默认为.
        fail_response_file_path:Path,失败的返回值写入的文件路径,输入为str或者Path,结果为Path类型,.开头为当前目录,以$开头为相对路径,如果开头没有.或者$,默认为.
        insert_error_file_path:Path,数据库写入失败的数据保存位置,输入为str或者Path,结果为Path类型,.开头为当前目录,以$开头为相对路径,如果开头没有.或者$,默认为.
    """
    source_data_file_path:Path
    source_data_dir_path:Path
    verify_data_file_path:Path
    verify_data_dir_path:Path
    success_response_file_path:Path
    fail_response_file_path:Path
    insert_error_file_path:Path
    @validator
    def __init__(self,*,source_data_file_path:Path|str,
                 source_data_dir_path:Path|str,
                 verify_data_file_path:Path|str,
                 verify_data_dir_path:Path|str,
                 success_response_file_path:Path|str,
                 fail_response_file_path:Path|str,
                 insert_error_file_path:Path|str)->"FileConfig":
        temp_dict = {}
        for key,value in locals().items():
            if key == "self":
                continue
            if key == "temp_dict":
                continue
            if isinstance(value,str):
                
                
                if 'file_path' in key:
                    temp_dict[key] = get_abs_file_path(value)
                elif 'dir_path' in key:
                    temp_dict[key] = get_abs_dir_path(value)
                else:
                    raise Exception(f"FileConfig初始化失败{key}不包含file_path或dir_path")
            else:
                temp_dict[key] = value
        return super().__init__(**temp_dict)
    def mapping_from_toml(cls,toml_config:dict) -> "FileConfig":
        ...


class BaseReadProcessConfig(BaseModel):
    """
    
    基础读取配置
    
    params:
        is_xlsx_save:bool,是否进行xlsx保存,默认为False
        is_muti_sheet_read:bool,是否从源文件读入全部sheet数据,默认为False
        is_dir_read:bool,是否读取指定目录下的所有文件,默认为False
        dir_read_ext:list[str],读取目录下的文件类型,在is_dir_read为True时才生效,默认为["xlsx"]
        is_combine_source_data:bool,是否合并源数据,默认为False
    """
    is_xlsx_save:bool = False
    is_muti_sheet_read:bool = False
    is_dir_read:bool = False
    dir_read_ext:list[str] = ['xlsx']
    is_combine_source_data:bool = False
    

class ProcessConfig(BaseModel):
    """
    
    流程控制配置
    
    params:
        is_db_save:bool,是否进行数据库保存,默认为True
        is_verify:bool,是否进行验证,默认为False
        source_data_process_config:BaseReadProcessConfig
        verify_data_process_config:BaseReadProcessConfig
        BaseReadProcessConfig
        params:
            is_xlsx_save:bool,是否进行xlsx保存,默认为False
            is_muti_sheet_read:bool,是否从源文件读入全部sheet数据,默认为False
            is_dir_read:bool,是否读取指定目录下的所有文件,默认为False
            dir_read_ext:list[str],读取目录下的文件类型,在is_dir_read为True时才生效,默认为["xlsx"]
            is_combine_source_data:bool,是否合并源数据,默认为False
    """
    is_db_save:bool  = True
    is_verify:bool = False
    source_data_process_config:BaseReadProcessConfig
    verify_data_process_config:BaseReadProcessConfig

class ConfigDTO(BaseModel):
    """
    配置DTO
    
    params:
    
        ai_model_config:AiModelConfig,Ai模型配置信息
        file_config:FileConfig,文件配置信息
        process_config:ProcessConfig,处理流程控制信息
    """
    ai_model_config:AiModelConfig
    file_config:FileConfig
    process_config:ProcessConfig
