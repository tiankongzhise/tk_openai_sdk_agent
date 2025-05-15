import sys
import traceback
def get_error_detail(exception=None):
    """
    获取异常的完整堆栈信息（字符串形式）
    :param exception: 可选，传入异常对象（若为 None，则自动获取当前异常）
    """
    if exception is None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
    else:
        exc_type = type(exception)
        exc_value = exception
        exc_traceback = exception.__traceback__
    error_msg = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return "".join(error_msg)
