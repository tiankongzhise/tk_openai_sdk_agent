from openai import OpenAI
from openai import AsyncOpenAI
from ..message import message
from contextlib import nullcontext

import os
import asyncio

class AgentWithSdk(object):
    def __init__(self, *args, **kwargs):
        self.system_content: str | None = kwargs.get("system_content")
        self.prompt: str | None = kwargs.get("prompt")
        self.ai_model: str | None = kwargs.get("ai_model")
        self.ai_model_mapping: str | None = kwargs.get("ai_model_mapping")
        self.stream: bool = kwargs.get("stream", False)
        self.print_console: bool = kwargs.get("print_console", False)
        self.client = OpenAI(
            api_key=os.environ.get("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3",
        )
        self.args: tuple = args
        self.kwargs: dict = kwargs

    def set_system_content(self, system_content: str):
        self.system_content = system_content

    def set_prompt(self, prompt: str):
        self.prompt = prompt

    def set_ai_model(self, ai_model: str):
        self.ai_model = ai_model

    def set_model_mapping(self, model_mapping: dict):
        self.ai_model_mapping = model_mapping

    def set_stream(self, stream: bool):
        self.stream = stream

    def set_print_console(self, print_console: bool):
        self.print_console = print_console

    def run(self, *args, **kwargs):
        model_id = self.ai_model_mapping.get(self.ai_model)
        if model_id is None:
            raise ValueError(
                f"Invalid ai_model:{self.ai_model},ai_model must be one of {list(self.ai_model_mapping.keys())}"
            )
        message.info("----- agent run request -----")
        chat_item = self.client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": self.system_content},
                {"role": "user", "content": self.prompt},
            ],
            # 免费开启推理会话应用层加密，访问 https://www.volcengine.com/docs/82379/1389905 了解更多
            # extra_headers={'x-is-encrypted': 'true'},
            # 响应内容是否流式返回
            stream=self.stream,
        )
        if self.stream:
            rsp = ""
            for chunk in chat_item:
                if not chunk.choices:
                    continue
                rsp += chunk.choices[0].delta.content
                if self.print_console:
                    message.print(chunk.choices[0].delta.content, end="")
        else:
            rsp = chat_item.choices[0].message.content
            if self.print_console:
                message.info(rsp)
        message.info("----agent rsp end----")
        return rsp


class SyncAgentWithSdk(AgentWithSdk):
    def __init__(self, *args, **kwargs):
        self.system_content: str | None = kwargs.get("system_content")
        self.prompt: str | None = kwargs.get("prompt")
        self.ai_model: str | None = kwargs.get("ai_model")
        self.ai_model_mapping: dict | None = kwargs.get("ai_model_mapping")
        self.stream: bool = kwargs.get("stream", False)
        self.print_console: bool = kwargs.get("print_console", False)
        self.prompt_template: str | None = kwargs.get("prompt_template")
        self.semaphore: asyncio.Semaphore | None = kwargs.get("semaphore")
        # 初始化Ark客户端，从环境变量中读取您的API Key
        self.client = AsyncOpenAI(
            api_key=os.environ.get("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3",
        )

        self.args: tuple = args
        self.kwargs: dict = kwargs

    def set_system_content(self, system_content: str):
        self.system_content = system_content

    def set_prompt(self, prompt: str):
        self.prompt = prompt

    def set_ai_model(self, ai_model: str):
        self.ai_model = ai_model

    def set_model_mapping(self, model_mapping: dict):
        self.ai_model_mapping = model_mapping

    def set_stream(self, stream: bool):
        self.stream = stream

    def set_print_console(self, print_console: bool):
        self.print_console = print_console

    async def run(self, *args, **kwargs):
        model_id =self.ai_model_mapping[kwargs.get('ai_model')] or self.ai_model_mapping.get(self.ai_model)
        if model_id is None:
            raise ValueError(
                f"Invalid ai_model:{self.ai_model},ai_model must be one of {list(self.ai_model_mapping.keys())}"
            )
        
        # 使用 nullcontext 兼容有无信号量的情况
        ctx = self.semaphore if isinstance(self.semaphore, asyncio.Semaphore) else nullcontext()
        async with ctx:
            message.info("----- agent run request -----")
            chat_item = await self.client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": self.system_content},
                    {"role": "user", "content": self.prompt},
                ],
                # 响应内容是否流式返回
                stream=self.stream,
                timeout=300
            )
            if self.stream:
                rsp = ""
                async for chunk in chat_item:
                    if not chunk.choices:
                        continue
                    rsp += chunk.choices[0].delta.content
                    if self.print_console:
                        message.print(chunk.choices[0].delta.content, end="")
            else:
                rsp = chat_item.choices[0].message.content
                if self.print_console:
                    message.info(rsp)
            message.info("----agent rsp end----")
            return rsp
