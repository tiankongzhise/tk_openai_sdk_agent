from .models import DuplicateDTO,DuplicateVerifyDTO
from .core import AsyncLLMResponseFetcher,AsyncMultiLLMResultVerifier
from .multi_process_save import MultiProcessSave
from ...message import message
from datetime import datetime
import asyncio
def core(data:DuplicateDTO):
    ...




async def async_fetch_data(data:dict[str,DuplicateDTO]):
    tasks = []
    # 通过第一个duplicate_dto获取配置信息
    first_duplicate_dto = next(iter(data.values()))
    # 获取批查询的数量大小
    query_batch_size = first_duplicate_dto.toml_config["BATCH_SIZE"]
    # 获取最大并发数
    semphore_number = first_duplicate_dto.toml_config["SEMAPHORE_NUMBER"]
    # 使用semaphore控制并发数
    semphore = asyncio.Semaphore(semphore_number)
    # 创建一个异步大模型客户端
    llm_client = AsyncLLMResponseFetcher(first_duplicate_dto)
    # 创建一个多进程保存器
    saver = MultiProcessSave(first_duplicate_dto.toml_config)
    
    # 提交异步查询任务
    for ai_model,duplicate_dto in data.items():
        message.info(f'{ai_model}开始,{len(duplicate_dto.data)}需要处理')
        for i in range(0,len(duplicate_dto.data),query_batch_size):
            chunck_data = duplicate_dto.data[i:i+query_batch_size]
            tasks.append(llm_client.run(chunck_data,ai_model,semphore))
        message.info(f'{ai_model}任务已经提交完毕')
    saver.start_process()
    
    total_time = 0.0
    complete_task_count = 0
    latest_task_count = 0.0
    for coro  in asyncio.as_completed(tasks):
        start_time = datetime.now()
        rsp = await coro
        saver.send_data(rsp)
        end_time = datetime.now()
        cost = (end_time - start_time).total_seconds()
        total_time += cost
        complete_task_count += 1
        message.info(
        f'总任务: {len(tasks)}, 完成: {complete_task_count}, '
        f'完成率: {complete_task_count/len(tasks)*100:.2f}%, '
        f'总耗时: {total_time:.2f}s, '
        f'平均耗时: {total_time/complete_task_count:.2f}s, '
        f'本次耗时: {cost:.2f}s, '
        f'上次耗时: {latest_task_count:.2f}s\n',
        end='\r'  # 修正为 \r（不是 /r）
    )
        latest_task_count = cost
    message.info('全部任务完成')
           
    # result= await ark_agent.run(test_ip_role_pairs)
    # saver.send_data(result)
    saver.join_process()
    
    return True
        
    
    
async def async_core(data:dict[str,DuplicateDTO]):
    return await async_fetch_data(data)    



async def async_verify_data(data:dict[str,DuplicateVerifyDTO]):
    tasks = []
    # 通过第一个DuplicateVerifyDTO获取配置信息
    first_duplicate_dto = next(iter(data.values()))
    # 获取批查询的数量大小
    query_batch_size = first_duplicate_dto.toml_config["BATCH_SIZE"]
    # 获取最大并发数
    semphore_number = first_duplicate_dto.toml_config["SEMAPHORE_NUMBER"]
    # 使用semaphore控制并发数
    semphore = asyncio.Semaphore(semphore_number)
    # 创建一个异步大模型客户端
    llm_client = AsyncMultiLLMResultVerifier(first_duplicate_dto)
    # 创建一个多进程保存器
    saver = MultiProcessSave(first_duplicate_dto.toml_config)
    
    # 提交异步查询任务
    for ai_model,duplicate_dto in data.items():
        message.info(f'{ai_model}开始,{len(duplicate_dto.data)}需要处理')
        for i in range(0,len(duplicate_dto.data),query_batch_size):
            chunck_data = duplicate_dto.data[i:i+query_batch_size]
            tasks.append(llm_client.run(chunck_data,ai_model,semphore))
        message.info(f'{ai_model}任务已经提交完毕')
    saver.start_process()
    
    total_time = 0.0
    complete_task_count = 0
    latest_task_count = 0.0
    for coro  in asyncio.as_completed(tasks):
        start_time = datetime.now()
        rsp = await coro
        saver.send_data(rsp)
        end_time = datetime.now()
        cost = (end_time - start_time).total_seconds()
        total_time += cost
        complete_task_count += 1
        message.info(
        f'总任务: {len(tasks)}, 完成: {complete_task_count}, '
        f'完成率: {complete_task_count/len(tasks)*100:.2f}%, '
        f'总耗时: {total_time:.2f}s, '
        f'平均耗时: {total_time/complete_task_count:.2f}s, '
        f'本次耗时: {cost:.2f}s, '
        f'上次耗时: {latest_task_count:.2f}s\n',
        end='\r'  # 修正为 \r（不是 /r）
    )
        latest_task_count = cost
    message.info('全部任务完成')
           
    # result= await ark_agent.run(test_ip_role_pairs)
    # saver.send_data(result)
    saver.join_process()
    
    return True
        

