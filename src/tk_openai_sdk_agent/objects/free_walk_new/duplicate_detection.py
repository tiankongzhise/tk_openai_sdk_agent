from .models import PreWorkDTO,DuplicateDTO,PreVerifyDTO,DuplicateVerifyDTO
from ...message import message
from ...database import Curd,DbOrmBaseMixin
from .db_models import aimodel_orm_mapping


from typing import Type
from sqlalchemy import select,delete

def deduplicate_prework_dto(data: PreWorkDTO) -> DuplicateDTO:
    """
    对预处理数据进行去重,如果ip和character都相同的数据，则认为是重复的
    params:
        data: PreWorkDTO
    returns:
        DuplicateDTO
    """
    
    if data.status != "success":
        raise ValueError(f"pre_work_dto status is not success,{data.message}")
    
    ip_character_pairs= set()
    new_data = []
    del_duplicate_count = 0
    for item in data.data:
        if f"{item.ip}@{item.character}" in ip_character_pairs:
            del_duplicate_count += 1
            continue
        else:
            ip_character_pairs.add(f"{item.ip}@{item.character}")
            new_data.append(item)
    if del_duplicate_count > 0:
        message.info(f'local_item_duplicate_detection删除了{del_duplicate_count}个重复元素')
    return DuplicateDTO(data=new_data,
                        extra_info=data.extra_info,
                        message=f'local_item_duplicate_detection删除了{del_duplicate_count}个重复元素,原始message:{data.message}',
                        status="success",
                        toml_config=data.toml_config)

def exclude_existing_in_db(data:DuplicateDTO,db_client:Curd,db_orm:Type[DbOrmBaseMixin]) -> DuplicateDTO:
    """
    过滤数据库中存在的元素
    params:
        data: DuplicateDTO,已经对预处理数据进行去重的数据
        db_client: Curd
        db_orm: Type[DbOrmBaseMixin]
    returns:
        DuplicateDTO
    """
    if data.status != "success":
        raise ValueError(f"DuplicateDTO status is not success,{data.message}")
    db_client = Curd()
    session_func = db_client.get_session()
    existing_db_set = set()
    new_data = []
    message.info(f'正在检测{db_orm.__tablename__}表是否存在重复元素')
    filter_count = 0
    with session_func() as session:
        del_stmt = delete(db_orm).where(db_orm.ai_rsp=="未知")
        del_records = session.execute(del_stmt)
        message.print(f'table:{db_orm.__tablename__}删除了{del_records.rowcount}条未知记录')
        session.flush()
        stmt = select(db_orm)
        db_result = session.execute(stmt).scalars().all()
        message.info(f'{db_orm.__tablename__}表共有{len(db_result)}条记录')
        for record in db_result:
            existing_db_set.add(f"{record.ip}@{record.character}")
    for item in data.data:
        if f"{item.ip}@{item.character}" in existing_db_set:
            filter_count += 1
            continue
        else:
            new_data.append(item)
    message.info(f'有{filter_count}个元素已经存在在{db_orm.__tablename__}被过滤掉,剩下{len(new_data)}个元素')
    return DuplicateDTO(data=new_data,
                        extra_info=data.extra_info,
                        message=f'exclude_existing_in_db{filter_count}个重复元素,原始message:{data.message}',
                        status="success",
                        toml_config=data.toml_config)
    
def duplicate_detection(data: PreWorkDTO,ai_model_items:list[str]|str|None = None,db_client:Curd = Curd) -> dict[str,DuplicateDTO]:
    """
    去重功能，返回一个字典，key是ai_model_name，value是去重后的数据
    首先对预处理的数据进行去重，然后对去重后的数据进行数据库去重
    params:
        data: PreWorkDTO
        ai_model_items: list[str]|str|None,如果ai_model_items为None，则使用toml_config中的AI_MODEL_LIST
        db_client: Curd: 默认使用Curd
    returns:
        dict[str,DuplicateDTO],key是ai_model_name，value是去重后的数据
    """
    temp = deduplicate_prework_dto(data)
    if ai_model_items is None:
        ai_model_items = temp.toml_config['AI_MODEL_LIST']
    if isinstance(ai_model_items,str):
        ai_model_items = [ai_model_items]
    
    temp_dict = {}
    for ai_model in ai_model_items:
        db_orm = aimodel_orm_mapping[ai_model]
        temp_dict[ai_model] = exclude_existing_in_db(temp,db_client,db_orm)
    
    result = temp_dict
    
    return result




def deduplicate_pre_verify_dto(data: PreVerifyDTO) -> DuplicateVerifyDTO:
    """
    对预处理数据进行去重,如果ip和character都相同的数据，则认为是重复的
    params:
        data: PreWorkDTO
    returns:
        DuplicateDTO
    """
    
    if data.status != "success":
        raise ValueError(f"pre_work_dto status is not success,{data.message}")
    
    ip_character_pairs= set()
    new_data = []
    del_duplicate_count = 0
    for item in data.data:
        if f"{item.ip}@{item.character}" in ip_character_pairs:
            del_duplicate_count += 1
            continue
        else:
            ip_character_pairs.add(f"{item.ip}@{item.character}")
            new_data.append(item)
    if del_duplicate_count > 0:
        message.info(f'deduplicate_pre_verify_dto删除了{del_duplicate_count}个重复元素')
    return DuplicateVerifyDTO(data=new_data,
                        extra_info=data.extra_info,
                        message=f'deduplicate_pre_verify_dto删除了{del_duplicate_count}个重复元素,原始message:{data.message}',
                        status="success",
                        toml_config=data.toml_config)

def verify_exclude_existing_in_db(data:DuplicateVerifyDTO,db_client:Curd,db_orm:Type[DbOrmBaseMixin]) -> DuplicateVerifyDTO:
    """
    过滤数据库中存在的元素
    params:
        data: DuplicateVerifyDTO,已经对预处理数据进行去重的数据
        db_client: Curd
        db_orm: Type[DbOrmBaseMixin]
    returns:
        DuplicateVerifyDTO
    """
    if data.status != "success":
        raise ValueError(f"DuplicateVerifyDTO status is not success,{data.message}")
    db_client = Curd()
    session_func = db_client.get_session()
    existing_db_set = set()
    new_data = []
    message.info(f'正在检测{db_orm.__tablename__}表是否存在重复元素')
    filter_count = 0
    with session_func() as session:
        # del_stmt = delete(db_orm).where(db_orm.ai_rsp=="未知")
        # del_records = session.execute(del_stmt)
        # message.print(f'table:{db_orm.__tablename__}删除了{del_records.rowcount}条未知记录')
        # session.flush()
        stmt = select(db_orm)
        db_result = session.execute(stmt).scalars().all()
        message.info(f'{db_orm.__tablename__}表共有{len(db_result)}条记录')
        for record in db_result:
            existing_db_set.add(f"{record.ip}@{record.character}")
    for item in data.data:
        if f"{item.ip}@{item.character}" in existing_db_set:
            filter_count += 1
            continue
        else:
            new_data.append(item)
    message.info(f'有{filter_count}个元素已经存在在{db_orm.__tablename__}被过滤掉,剩下{len(new_data)}个元素')
    return DuplicateVerifyDTO(data=new_data,
                        extra_info=data.extra_info,
                        message=f'exclude_existing_in_db{filter_count}个重复元素,原始message:{data.message}',
                        status="success",
                        toml_config=data.toml_config)
    
def duplicate_verify_detection(data: PreVerifyDTO,ai_model_items:list[str]|str|None = None,db_client:Curd = Curd) -> dict[str,DuplicateVerifyDTO]:
    """
    去重功能，返回一个字典，key是ai_model_name，value是去重后的数据
    首先对预处理的数据进行去重，然后对去重后的数据进行数据库去重
    params:
        data: PreWorkDTO
        ai_model_items: list[str]|str|None,如果ai_model_items为None，则使用toml_config中的AI_MODEL_LIST
        db_client: Curd: 默认使用Curd
    returns:
        dict[str,DuplicateDTO],key是ai_model_name，value是去重后的数据
    """
    temp = deduplicate_pre_verify_dto(data)
    if ai_model_items is None:
        ai_model_items = temp.toml_config['VERIFY_AI_MODEL']
    if isinstance(ai_model_items,str):
        ai_model_items = [ai_model_items]
    
    temp_dict = {}
    for ai_model in ai_model_items:
        db_orm = aimodel_orm_mapping[ai_model]
        temp_dict[ai_model] = verify_exclude_existing_in_db(temp,db_client,db_orm)
    
    result = temp_dict
    
    return result

