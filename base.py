#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName     :base.py
# @Time         :2025/10/9 17:18
# @Author       :https://github.com/vincenschan/
# @Description  : 


from contextlib import contextmanager
import time
import openai
import re
import numpy as np

@contextmanager
def timer(name="任务"):
    start = time.perf_counter()
    yield
    print(f"[{name}] 耗时: {time.perf_counter() - start:.3f}秒")


class InfrenceBase:
    def __init__(self):
        pass

    def inference(self, text, **kwargs):
        raise NotImplementedError


def openai_inf(prompt, base_url, model, api_key, return_prob=False):
    """
    base_url="https://deepbank-llm.daikuan.qihoo.net",
    model="deepbank/qwen3-32b",
    api_key="sk-a2739df0-0e46-49ae-b9ea-f06f174ba1fe"

    api_key='sk-8abb85890ec44cc295a48d4792280b55',
    base_url="http://deepbank-llm.daikuan.qihoo.net/v1",
    model='360/gpt-4.1'
    """
    client = openai.OpenAI(
        api_key=api_key,  # 请替换为您创建的个人key
        base_url=base_url  # 模型网关提供的访问接口
    )

    prompt = prompt + "/no_think" if "qwen3" in model.lower() else prompt

    response = ""
    if return_prob:
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=1.0,
            n=1,
            logprobs=True
        )
    else:
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=1.0,
        )
    data_json = response.model_dump()
    response_text = data_json['choices'][0]["message"]["content"]
    if "qwen3" in model.lower():
        response_text = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)

    perplexity = 1000
    if return_prob:
        ans_logps = [item["logprob"] for item in data_json['choices'][0]["logprobs"]["content"]]
        ans_logps = np.clip(ans_logps, -2.0, 0.0)
        perplexity = -np.mean(ans_logps) if len(ans_logps) > 0 else 1000.0

    return response_text.replace("\n\n", "\n"), perplexity

if __name__ == "__main__":
    pass
