from src.tk_openai_sdk_agent.objects.free_walk_new import async_run,run

import asyncio


if __name__ == '__main__':
    
    
    # async_result = asyncio.run(async_run())
    # print(async_result)

    result = run()
    print(result)
