#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName     :vllm_inference.py
# @Time         :2025/10/9 17:17
# @Author       :https://github.com/vincenschan/
# @Description  :

import json
import requests
import re
import json
from .base import timer

"""
CUDA_VISIBLE_DEVICES=0 python3 -m vllm.entrypoints.openai.api_server --model Qwen3-8B --trust-remote-code --port 8000

CUDA_VISIBLE_DEVICES=1 python3 -m vllm.entrypoints.openai.api_server --model Qwen3-14B --trust-remote-code --port 8001

CUDA_VISIBLE_DEVICES=0,1 python3 -m vllm.entrypoints.openai.api_server --model Qwen3-30B --trust-remote-code --tensor-parallel-size 2 --port 8000 --max-num-batched-tokens 8192 --disable-torch-compile 
"""


class VLLMInference():

    def inference(self, url, model_name, sys_prompt, user_content, return_json=False, **kwargs):
        """
        LLM VLLM & SGLANG 私有化部署，通过API调用
        部署脚本example:
            python3 -m vllm.entrypoints.openai.api_server --model /path/to/Qwen-7B-Chat --trust-remote-code --port 8000
        :param url: 模型部署的URL
        :param model_name: 模型名称
        :param sys_prompt:
        :param user_content:
        :param return_json: 是否需要返回原始json结果
        :param kwargs:
        :return:
        """
        url = url + "/v1/chat/completions"
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_content}
            ],
        }
        if 'max_tokens' in kwargs:
            default_max_tokens = 32000 if "qwen3" in model_name.lower() else 8192
            max_tokens = kwargs.get('max_tokens', default_max_tokens)
            payload.update({"max_tokens": max_tokens})
        if "thought_control" in kwargs:
            payload.update({"thought_control": kwargs.get('thought_control', {
                "enable": False,
                "max_thought_tokens": 0  # 强制0思考token
            })})
        if "temperature" in kwargs:
            payload.update({"temperature": kwargs.get('temperature', 1)})

        resp = requests.post(url, json=payload)
        # print(f"URL: {url}, response: {resp}")
        response_json = resp.json()

        if not return_json and "qwen3" in model_name.lower():
            response = response_json['choices'][0]["message"]["content"]
            response_no_think = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
            # print(f"**Output: {response}, no_think: {response_no_think}")
            return response_no_think
        return return_json

    def inference_embed(self, url, model_name, prompt, content):
        """
        Embedding模型 VLLM & SGLANG 私有化部署，通过API调用
        python3 -m vllm.entrypoints.openai.api_server --model /path/to/Qwen-7B-Chat --trust-remote-code --port 8000
        :param url:
        :param model_name:
        :param prompt:
        :param content:
        :return:
        """
        url = url + "/embeddings"
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            "temperature": 0.5,
            # "max_tokens": 256,
            "thought_control": {
                "enable": False,
                "max_thought_tokens": 0  # 强制0思考token
            }
        }
        response = requests.post(url, json=payload)
        # print("**Output: %s" % response.json()["content"])
        return response.json()["content"]


    def bge_embedding(self, contents: list, url="http://localhost:5000/v1/embeddings", model_name="bge-m3", **kwargs):
        """

        :param contents: LIST格式
        :param url:
        :param model_name:
        :return:
        """

        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": model_name,
            "input": contents
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        embeddings = []
        if response.status_code == 200:
            results = response.json().get("data", [])
            for i, item in enumerate(results):
                vector = item["embedding"]
                embeddings.append(vector)
                print(f"文本: {contents[i]}")
                print(f"向量长度: {len(vector)}")
                print(f"前5维示例: {vector[:5]}")
                print("-" * 40)
        else:
            print(f"请求失败，状态码：{response.status_code}")
        return response


if __name__ == "__main__":
    MODELS = {
        "QWen3-8B": {
            'api_key': '-',
            'base_url': "http://0.0.0.0:8000/v1",
            'model_name': "/home/jovyan/vincens/models/models/Qwen3-8B"
        },
        "QWen3-14B": {
            'api_key': '-',
            'base_url': "http://0.0.0.0:8001/v1",
            'model_name': "/home/jovyan/vincens/models/models/Qwen3-14B"
        },
    }
    content = "你是谁"
    model_name = "QWen3-8B"
    with timer(model_name):
        response = VLLMInference().inference(url=MODELS[model_name]["base_url"],
                                             model_name=MODELS[model_name]["model_name"], prompt="你是谁",
                                             content=content)
        print(response)
