import os
import json
import openai
import random
from typing import List, Tuple, Dict, Optional
from abc import ABC, abstractmethod
from data_utils import load_datasets, get_table_schema

class LLMBackend(ABC):
    """
    Абстрактный класс для backend'ов языковых моделей.
    Все наследники должны реализовать метод `generate`.
    """
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class YandexGPTBackend(LLMBackend):
    """
    Реализация backend'а для YandexGPT через API Cloud Yandex.
    """
    def __init__(self, folder_id: str, api_key: str, model: str = "llama"):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://llm.api.cloud.yandex.net/v1"
        )
        self.folder_id = folder_id
        self.model = model

    def generate(self, prompt: str = None, messages: List[Dict[str, str]] = None) -> str:
        if messages is None:
            messages = [{"role": "user", "content": prompt}]

        response = self.client.chat.completions.create(
            model=f"gpt://{self.folder_id}/{self.model}",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": False},
            },
        )
        if not response or not response.choices:
            raise ValueError("Empty response from model")
        return response.choices[0].message.content or ""


class VLLMBackend(LLMBackend):
    """
    Реализация backend'а для локального сервера vLLM (open source inference).
    """
    def __init__(self, model: str = "RedHatAI/DeepSeek-R1-Distill-Qwen-32B-quantized.w4a16", **kwargs):
        from vllm import LLM, SamplingParams
        self.llm = LLM(model=model, **kwargs)
        self.sampling_params = SamplingParams(
            temperature=0.7,
            max_tokens=3000,
        )

    def generate(self, prompt: str = None, messages: List[Dict[str, str]] = None) -> str:
        response = None
        if messages is None:
            response = self.llm.generate([prompt], self.sampling_params)
        else:
            response = self.llm.chat(messages, self.sampling_params)
        if not response or not response[0].outputs[0].text:
            raise ValueError("Empty response from model")
        return response[0].outputs[0].text or ""