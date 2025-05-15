from pathlib import Path
from typing import Any, Generator


from tk_base_utils import get_abs_file_path
from tk_base_utils import load_toml,get_target_file_path

from .models import FreeWalkSourceData,FreeWalkSourceDTO,PreWorkDTO,VerifySourceData,PreVerifyDTO

import pandas as pd


def get_config() -> dict[str, Any]:
    config_path = get_target_file_path("config.toml")
    toml_config = load_toml(config_path)
    return toml_config


def get_source_data(source_file_path: str|Path) -> FreeWalkSourceDTO:
    if isinstance(source_file_path,str):
        source_file_path = get_abs_file_path(source_file_path)
    df = pd.read_excel(source_file_path, sheet_name="Sheet1")
    ip_list = df['IP'].to_list()
    character_list = df['角色'].to_list()
    def _get_source_data() -> Generator[FreeWalkSourceData, Any, None]:
        for ip,character in zip(ip_list,character_list):
            yield FreeWalkSourceData(ip=ip,character=character)
    return FreeWalkSourceDTO(
        status="success",
        message="get_source_data return success",
        extra_info={},
        data=_get_source_data())



def pre_process(*args,**kwargs):
    toml_config = get_config()
    source_data_file_path  = toml_config.get("SOURCE_DATA_FILE_PATH")
    source_data = get_source_data(source_data_file_path)
    
    
    return PreWorkDTO(
        status="success",
        message="pre_process return success",
        extra_info={},
        data=list(source_data.data),
        toml_config=toml_config)
    
    
 
def get_verify_source_data(source_file_path: str|Path) -> Generator[VerifySourceData, Any, None]:
    if isinstance(source_file_path,str):
        source_file_path = get_abs_file_path(source_file_path)
    df = pd.read_excel(source_file_path, sheet_name="Sheet1")
    records = df.to_dict(orient="records")
    
    def _get_source_data() -> Generator[VerifySourceData, Any, None]:
        for record in records:
            yield VerifySourceData(**record)
    return _get_source_data()   


def pre_verify_process(*args,**kwargs):
    toml_config = get_config()
    source_data_file_path  = toml_config["VERIFY_SOURCE_DATA_FILE_PATH"]
    source_data = get_verify_source_data(source_data_file_path)
    
    
    return PreVerifyDTO(
        status="success",
        message="pre_verify_process return success",
        extra_info={},
        data=list(source_data),
        toml_config=toml_config)
