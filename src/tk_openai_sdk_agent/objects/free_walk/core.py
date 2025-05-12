from tk_base_utils import load_toml,get_current_dir_path


from ...core import SyncAgentWithSdk

from ...utils import fomart_rsp_str

from ...models import AgentSetting,Response,RspResult
from ...message import message

from copy import deepcopy
import json
import asyncio
class SyncArkAgent(SyncAgentWithSdk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def set_agent_toml(self) -> dict:
        """
        从当前路径下的config.toml文件中获取agent的配置信息,
        并将配置信息保存到self.agent_toml中
        返回None
        """
        current_path = get_current_dir_path()
        toml_file_path = current_path / 'config.toml'
        self.agent_toml =  load_toml(toml_file_path)
    
    def set_agent_setting(self):
        self.set_agent_toml()
        agent_setting =  AgentSetting.toml_mapping(self.agent_toml)
        agent_setting = agent_setting.model_dump()
        for k,v in agent_setting.items():
            setattr(self,k,v)
    
    def set_prompt(self, ip_role_pairs):
        prompt_template = deepcopy(self.prompt_template)
        prompt_template = prompt_template.replace("{{IP_ROLE_PAIRS}}", "\n".join(ip_role_pairs))
        super().set_prompt(prompt_template)
    
    def set_semaphore(self):
        semaphore_number = self.semaphore_number
        self.semaphore = asyncio.Semaphore(semaphore_number)
    async def run(self,ip_role_pairs:list[str],ai_model:str|None = None) -> RspResult:
        self.set_agent_setting()
        self.set_prompt(ip_role_pairs)
        self.set_semaphore()
        try:
            if ai_model:
                rsp = await super().run(ai_model=ai_model)
            else:
                rsp = await super().run()
        except Exception as e:
            return RspResult(fail_data=f'模型调用失败,错误原因{str(e)},调用模型{ai_model},prompt:{self.prompt},',message=str(e),status="fail")
        try:
            fomated_rsp_str = fomart_rsp_str(rsp)
            rsp_dict = json.loads(fomated_rsp_str)
            response = []
            if isinstance(rsp_dict,list):
                for item in rsp_dict:
                    try:
                        response.append(Response(**{**item,'ai_model':ai_model}))
                    except ValueError as e:
                        message.print(f"item is not a valid Response object:{item},error:{e}")
            elif isinstance(rsp_dict,dict):
                try:
                    response = [Response(**{**rsp_dict,'ai_model':ai_model})]
                except ValueError as e:
                    message.print(f"rsp_dict is not a valid Response object:{rsp_dict},error:{e}")
            else:
                raise ValueError(f"rsp_dict is not a list or dict:{rsp_dict}") 
            return RspResult(data=response,message="success",status="success")
        except Exception as e:
            return RspResult(fail_data=rsp+f'_@#ai_model={ai_model}',message=str(e),status="fail")
