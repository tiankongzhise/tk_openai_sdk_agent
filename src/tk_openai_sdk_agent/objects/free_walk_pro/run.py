from .pre_work import pre_process
from .duplicate_detection import duplicate_detection
from .main import core,async_core



def run():
    pre_dto = pre_process()
    duplicate_dto = duplicate_detection(pre_dto)
    final_result = core(duplicate_dto)
    result = final_result
    return result
    
async def async_run():
    pre_dto = pre_process()
    duplicate_dto = duplicate_detection(pre_dto)
    final_result = await async_core(duplicate_dto)
    result = final_result
    return result
