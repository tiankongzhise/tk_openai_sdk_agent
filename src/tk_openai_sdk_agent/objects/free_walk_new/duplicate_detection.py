from .models import PreWorkDTO,DuplicateDTO
from ...message import message
from ...database import Curd,MixedBase


from typing import Type
from sqlalchemy import select

def deduplicate_prework_dto(data: PreWorkDTO) -> DuplicateDTO:
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
                        status=data.status,
                        toml_config=data.toml_config)

def exclude_existing_in_db(data:DuplicateDTO,db_client:Curd,table_name:Type[MixedBase]):
    session_func = db_client.get_session()
    with session_func() as session:
        stmt = select(table_name)
        db_result = session.execute(stmt).scalars().all()
        message.info(f'{table_name.__tablename__}表共有{len(db_result)}条记录')
        for record in db_result:
            if record.ip == 
    
