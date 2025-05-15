from src.tk_openai_sdk_agent.database import Curd
from src.tk_openai_sdk_agent.objects.free_walk.run import get_source_data,get_abs_file_path
from src.tk_openai_sdk_agent.objects.free_walk_new.db_models import aimodel_orm_mapping
from src.tk_openai_sdk_agent.objects.free_walk_new.models import FreeWalkSourceData
from tk_base_utils import load_toml
from sqlalchemy import select
import pandas as pd

source_data = get_source_data('$/src/tk_openai_sdk_agent/data/成都世界线自由行数据.xlsx')
ip = source_data['IP'].to_list()
character = source_data['角色'].to_list()
result = []
for i,c in zip(ip,character):
    format_data = FreeWalkSourceData(ip=i,character=c)
    result.append({
        'IP':format_data.ip,
        "角色":format_data.character,
        "原始IP输入":i,
        "角色输入":c,
        "新匹配列":f'{format_data.ip}@{format_data.character}',
        "老匹配列":f'{i}@{c}'
    })
df = pd.DataFrame(result)

    
is_verify = True



temp_data_path = get_abs_file_path('$/src/tk_openai_sdk_agent/report/中间数据.xlsx')
save_path = get_abs_file_path('$/src/tk_openai_sdk_agent/report/最新报告.xlsx')
config_path = get_abs_file_path('$/src/tk_openai_sdk_agent/objects/free_walk_new/config.toml')
toml_config = load_toml(config_path)

temp_data_path.parent.mkdir(parents=True,exist_ok=True)
df.to_excel(temp_data_path,index=False)

ai_models = toml_config['AI_MODEL_LIST']
if is_verify:
    ai_models.append(toml_config['VERIFY_AI_MODEL'])

db_client = Curd()
session_func = db_client.get_session()

for ai_model in ai_models:
    print(f'正在查询{ai_model}的数据')
    table = aimodel_orm_mapping[ai_model]
    stmt = select(table)
    with session_func() as session:
        result = session.execute(stmt).scalars().all()
        print(f'ai_model:{ai_model},查询了{len(result)}条记录,开始整合进入source_data')
        # 将查询出来的结果根据ip和角色整合进入source_data.新增一列名称为ai_model的值,列的值为ai_rsp的值
        for row in result:
            df.loc[(df['IP'] == row.ip) & (df['角色'] == row.character), ai_model] = row.ai_rsp
        print(f'ai_model:{ai_model},整合完毕')

#对比四个模型的列的值,将第一个模型的值作为标准,统计匹配相同的次数

compare_cols = ai_models

for base_col in compare_cols:
    # 计算匹配数（仅比较指定列）
    df[f"{base_col}一致数量"] = df[compare_cols].eq(df[base_col], axis=0).sum(axis=1)
new_compare_cols = [f"{col}一致数量" for col in compare_cols]
df['ai一致数量'] =  df[new_compare_cols].max(axis=1)


save_path.parent.mkdir(parents=True, exist_ok=True)
df.to_excel(save_path, index=False)
