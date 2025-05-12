from typing import Any,Type

from dotenv import load_dotenv
from pathlib import Path
from tk_base_utils import get_abs_file_path, load_toml, get_target_file_path

from .core import SyncArkAgent
from ...message import message
from ...database import (Curd,
                         IpInfoDeepseekR1,
                         IpInfoDeepseekV3,
                         IpInfoDoubaoThinkPro,
                         IpInfoDoubaoVersionPro,
                         SqlAlChemyBase)
from ...utils import MultiProcessingSave,fomart_agent_rsp,MultiProcessSave
from sqlalchemy import delete

from datetime import datetime
import pandas as pd
import asyncio

load_dotenv()


def get_source_data(source_file_path: str) -> pd.DataFrame:
    """
    获取源数据
    :param source_file_path: 源数据文件路径,从配置文件读取以.或者$开头的路径,
    :return: 源数据
    """
    source_file_path = source_file_path or "source_data.csv"
    file_path = get_abs_file_path(source_file_path)
    df = pd.read_excel(file_path, sheet_name="Sheet1")
    return df


def get_config() -> dict[str, Any]:
    config_path = get_target_file_path("config.toml")
    toml_config = load_toml(config_path)
    return toml_config

def mapping_table(ai_model:str)->Type[SqlAlChemyBase]:
    """
    根据ai模型映射表获取映射表
    :param ai_model: ai模型
    :return: 映射表
    """
    mapping_dict = {
        'DEEPSEEK-R1': IpInfoDeepseekR1,
        'DEEPSEEK-V3': IpInfoDeepseekV3,
        'DOUBAO-THINKING-PRO': IpInfoDoubaoThinkPro,
        'DOUBAO-VISION-PRO': IpInfoDoubaoVersionPro,
    }
    return mapping_dict[ai_model]

def create_file_path(file_path:str)->Path:
    """
    创建文件路径
    :param file_path: 文件路径
    :return: 文件路径
    """
    file_path = Path(file_path)
    return file_path
def find_missing_combinations(input_str_list:list[str], ai_model:str, db_client:Type[Curd]) -> list[str]:
    """找出不在数据库中的IP-Character组合"""
    input_pairs = [s.split('-', 1) for s in input_str_list]
    input_ips = [pair[0] for pair in input_pairs]
    input_chars = [pair[1] for pair in input_pairs]
    session_func = db_client.get_session()
    model_class = mapping_table(ai_model)
    
    with session_func() as session:
        # 查询数据库中存在的组合
        existing = session.query(
            model_class.source_ip_query,
            model_class.source_character_query
        ).filter(
            model_class.source_ip_query.in_(input_ips),
            model_class.source_character_query.in_(input_chars)
        ).all()
        
        existing_set = {f"{ip}-{char}" for ip, char in existing}
    return [s for s in input_str_list if s not in existing_set]
def delete_unknown_records(db_client:Type[Curd],ai_models:list[str]):
    for ai_model in ai_models:
        model_class = mapping_table(ai_model)
        session_func = db_client.get_session()
        with session_func() as session:
            stmt = delete(model_class).where(model_class.ai_rsp=="未知")
            del_records = session.execute(stmt)
            message.print(f'ai_model:{ai_model},删除了{del_records.rowcount}条记录')

async def run():
    toml_config = get_config()
    source_data = get_source_data(toml_config.get("SOURCE_DATA_FILE_PATH"))
    ip = source_data["IP"].tolist()
    character = source_data["角色"].tolist()
    ip_role_pairs = [f"{i}-{j}" for i, j in zip(ip, character)]

    target_ip_role_pairs = ip_role_pairs
    
    ai_models = ["DEEPSEEK-R1","DEEPSEEK-V3","DOUBAO-THINKING-PRO","DOUBAO-VISION-PRO"]
    db_client = Curd()
    delete_unknown_records(db_client,ai_models)
    not_in_db_ip_role_pairs = {ai_model:find_missing_combinations(target_ip_role_pairs,ai_model,db_client) for ai_model in ai_models}
    
    ark_agent = SyncArkAgent()
    
    saver = MultiProcessSave(
        config=toml_config
    )
    
    saver.start_process()
    
    batch_size = toml_config.get("BATCH_SIZE")
    print(f'总数据量:{len(target_ip_role_pairs)}')
    
    total_time = 0.0
    complete_task_count = 0
    latest_task_count = 0.0
    tasks = []
    for ai_model in ai_models:
        model_to_insert = not_in_db_ip_role_pairs[ai_model]
        print(f'{ai_model}开始,{len(model_to_insert)}需要处理')
        for i in range(0,len(model_to_insert),batch_size):
            chunck_data = model_to_insert[i:i+batch_size]
            tasks.append(ark_agent.run(chunck_data,ai_model))
        print(f'{ai_model}任务已经提交完毕')
        

    for coro  in asyncio.as_completed(tasks):
        start_time = datetime.now()
        rsp = await coro
        saver.send_data(rsp)
        end_time = datetime.now()
        cost = (end_time - start_time).total_seconds()
        total_time += cost
        complete_task_count += 1
        print(
        f'总任务: {len(tasks)}, 完成: {complete_task_count}, '
        f'完成率: {complete_task_count/len(tasks)*100:.2f}%, '
        f'总耗时: {total_time:.2f}s, '
        f'平均耗时: {total_time/complete_task_count:.2f}s, '
        f'本次耗时: {cost:.2f}s, '
        f'上次耗时: {latest_task_count:.2f}s\n',
        end='\r'  # 修正为 \r（不是 /r）
    )
        latest_task_count = cost
    print('全部任务完成')
        
        
    # result= await ark_agent.run(test_ip_role_pairs)
    # saver.send_data(result)
    saver.join_process()

        
