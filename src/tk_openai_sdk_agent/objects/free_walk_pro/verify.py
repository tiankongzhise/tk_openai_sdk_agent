from .pre_work import pre_verify_process
from .duplicate_detection import duplicate_verify_detection
from .main import async_verify_data

async def async_run():
    pre_dto = pre_verify_process()
    duplicate_dto = duplicate_verify_detection(pre_dto)
    final_result = await async_verify_data(duplicate_dto)
    result = final_result
    return result
