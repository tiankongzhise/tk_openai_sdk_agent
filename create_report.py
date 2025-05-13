from src.tk_openai_sdk_agent.database import Curd
from src.tk_openai_sdk_agent.objects.free_walk.run import get_source_data,get_abs_file_path
from src.tk_openai_sdk_agent.objects.check_work.run import mapping_table
from sqlalchemy import select

source_data = get_source_data('$/src/tk_openai_sdk_agent/data/成都世界线自由行数据.xlsx')
save_path = get_abs_file_path('$/src/tk_openai_sdk_agent/report/最新报告.xlsx')

ai_models = ["DEEPSEEK-R1","DEEPSEEK-V3","DOUBAO-THINKING-PRO","DOUBAO-VISION-PRO",'DOUBAO-PRO-32K']
db_client = Curd()
session_func = db_client.get_session()

for ai_model in ai_models:
    print(f'正在查询{ai_model}的数据')
    table = mapping_table(ai_model)
    stmt = select(table)
    with session_func() as session:
        result = session.execute(stmt).scalars().all()
        print(f'ai_model:{ai_model},查询了{len(result)}条记录,开始整合进入source_data')
        # 将查询出来的结果根据ip和角色整合进入source_data.新增一列名称为ai_model的值,列的值为ai_rsp的值
        for row in result:
            source_data.loc[(source_data['IP'] == row.source_ip_query) & (source_data['角色'] == row.source_character_query), ai_model] = row.ai_rsp
        print(f'ai_model:{ai_model},整合完毕')

#对比四个模型的列的值,将第一个模型的值作为标准,统计匹配相同的次数

compare_cols = ["DEEPSEEK-V3","DEEPSEEK-R1", "DOUBAO-THINKING-PRO", "DOUBAO-VISION-PRO",'DOUBAO-PRO-32K']

for base_col in compare_cols:
    # 计算匹配数（仅比较指定列）
    source_data[f"{base_col}一致数量"] = source_data[compare_cols].eq(source_data[base_col], axis=0).sum(axis=1)
new_compare_cols = [f"{col}一致数量" for col in compare_cols]
source_data['ai一直数量'] =  source_data[new_compare_cols].max(axis=1)


save_path.parent.mkdir(parents=True, exist_ok=True)
source_data.to_excel(save_path, index=False)
